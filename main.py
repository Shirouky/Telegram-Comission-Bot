from telebot import TeleBot, types
from json import load, dump

with open("database.json", 'r') as database:
    data = load(database)

with open("text.json", 'r', encoding='utf-8') as t:
    text = load(t)

bot = TeleBot(data["bot_data"]["token"])
admin_chat_id = data["bot_data"]["admin_chat_id"]

bot.set_my_commands(
    commands=[
        types.BotCommand("delete", "Удалить лишний вопрос"),
        types.BotCommand("news", "Выложить новость"),
    ],
    scope=types.BotCommandScopeChat(admin_chat_id)
)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text["text_menu"]))
    bot.send_message(message.chat.id, text["hello"], reply_markup=markup, parse_mode="HTML")


@bot.message_handler(commands=["news"])
def create_news(message):
    for id_ in data["news"]:
        bot.copy_message(id_, admin_chat_id, message.reply_to_message.id)
    bot.send_message(admin_chat_id, text["admin_messages"]["news"])


@bot.message_handler(commands=["delete"])
def delete_question(message):
    if message.reply_to_message and message.chat.id == admin_chat_id:
        remove_from_db(message, "questions")
        remove_from_db(message, "phones")
    else:
        bot.send_message(message.chat.id, text["errors"]["reply"])


@bot.message_handler(content_types=["text", "photo"])
def show_menu(message):
    if message.text == text["text_menu"] and message.chat.id != admin_chat_id:
        news = str(message.chat.id in data["news"])
        keys = []
        buttons = list(text["menu"].keys())
        for button in buttons:
            title = text["menu"][button]
            keys.append([types.InlineKeyboardButton(title, callback_data=button)])
        keys.append([types.InlineKeyboardButton(text["news_buttons"][news]["button"],
                                                callback_data=text["news_buttons"][news]["call"])])
        keyboard = types.InlineKeyboardMarkup(keys)

        bot.send_message(message.chat.id, text["menu_ask"], reply_markup=keyboard)

    elif message.reply_to_message and message.chat.id == admin_chat_id:
        question = remove_from_db(message, "questions")
        bot.copy_message(question["chat_id"], admin_chat_id, message.id, reply_to_message_id=question["message_id"])
        remove_from_db(message, "phones")

    elif message.chat.id != admin_chat_id:
        bot.send_message(message.chat.id, text["errors"]["text"], reply_to_message_id=message.id)


@bot.callback_query_handler(func=lambda call: True)
def press_buttons(call):
    match call.data:
        case "questions" | "phones":
            ask_info(call.message, call.data)
        case "map":
            show_map(call.message)
        case "years":
            show_years(call.message)
        case "addnews":
            data["news"].append(call.message.chat.id)
            change_news(call.message)
        case "removenews":
            data["news"].remove(call.message.chat.id)
            change_news(call.message)
        case "faq":
            bot.delete_message(call.message.chat.id, call.message.id)
            faq(call.message)
        case "program":
            bot.delete_message(call.message.chat.id, call.message.id)
            faq_program(call.message)
        case "bi" | "sa":
            bot.delete_message(call.message.chat.id, call.message.id)
            faq_bi_sa(call.message, call.data)
        case "faculty" | "vsb" | "work" | "dorm" | "exams" | "other":
            bot.delete_message(call.message.chat.id, call.message.id)
            send_text(call.message, text["faq"][call.data]["text"], "faq")
        case "bi_ii" | "bi_ce" | "work_bi" | "vsb_bi" | "more_bi":
            bot.delete_message(call.message.chat.id, call.message.id)
            send_text(call.message, text["faq"]["program"]["bi"][call.data]["text"], "bi")
        case "sa_prog" | "work_sa" | "vsb_sa" | "more_sa":
            bot.delete_message(call.message.chat.id, call.message.id)
            send_text(call.message, text["faq"]["program"]["sa"][call.data]["text"], "sa")


def send_text(message, button_text, callback):
    keys = [[types.InlineKeyboardButton(text["text_back"], callback_data=callback)]]
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(message.chat.id, button_text, parse_mode="HTML", reply_markup=keyboard)


def faq(message):
    keys = [[types.InlineKeyboardButton(text["faq"]["faculty"]["title"], callback_data="faculty"),
             types.InlineKeyboardButton(text["faq"]["program"]["title"], callback_data="program")]]
    buttons = list(text["faq"].keys())[5:]
    for button in buttons:
        title = text["faq"][button]["title"]
        keys.append([types.InlineKeyboardButton(title, callback_data=button)])
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(message.chat.id, text["faq"]["text"], reply_markup=keyboard)


def faq_program(message):
    keys = []
    buttons = list(text["faq"]["program"].keys())[1:]
    for button in buttons:
        title = text["faq"]["program"][button]["title"]
        keys.append([types.InlineKeyboardButton(title, callback_data=button)])
    keys.append([types.InlineKeyboardButton(text["text_back"], callback_data="faq")])
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(message.chat.id, text["faq"]["text_program"], reply_markup=keyboard)


def faq_bi_sa(message, program):
    keys = []
    buttons = list(text["faq"]["program"][program].keys())[1:]
    for button in buttons:
        title = text["faq"]["program"][program][button]["title"]
        keys.append([types.InlineKeyboardButton(title, callback_data=button)])
    keys.append([types.InlineKeyboardButton(text["text_back"], callback_data="program")])
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(message.chat.id, text["faq"]["text_bi_sa"], reply_markup=keyboard)


def ask_info(message, request):
    bot.send_message(message.chat.id, text["ask"][request])
    bot.register_next_step_handler(message, get_info, request)


def get_info(message, request):
    if message.text != text["text_menu"]:
        bot.send_message(message.chat.id, text["thanks"][request])
        if check_in_db(message, "questions") and check_in_db(message, "phones"):
            bot.send_message(admin_chat_id, text["admin_messages"][request])
            admin_message = bot.forward_message(admin_chat_id, message.chat.id, message.id)
            bot.pin_chat_message(admin_chat_id, admin_message.id, disable_notification=False)
            request_data = {"chat_id": message.chat.id, "message_id": message.id,
                            "admin_chat_message_id": admin_message.id}
            data[request].append(request_data)
            update_db()
    else:
        show_menu(message)


def show_map(message):
    with open("map.png", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption=text["map"], parse_mode="HTML")


def show_years(message):
    with open("years.jpg", "rb") as photo:
        bot.delete_message(message.chat.id, message.id)
        keys = [[types.InlineKeyboardButton(text["text_back"], callback_data="faq")]]
        keyboard = types.InlineKeyboardMarkup(keys)
        bot.send_photo(message.chat.id, photo, caption=text["faq"]["years"]["text"], parse_mode="HTML", reply_markup=keyboard)


def change_news(message):
    update_db()
    subscribe = str(message.chat.id in data["news"])
    bot.send_message(message.chat.id, text["news_buttons"][subscribe]["text"])


def update_db():
    with open("database.json", "w") as f:
        dump(data, f)


def check_in_db(message, title):
    for elem in data[title]:
        if message.chat.id == elem["chat_id"] and message.id == elem["message_id"]:
            return False
    return True


def remove_from_db(message, title):
    for elem in data[title]:
        if message.reply_to_message.id == elem["admin_chat_message_id"]:
            bot.unpin_chat_message(admin_chat_id, message.reply_to_message.id)
            data[title].remove(elem)
            update_db()
            return elem


bot.infinity_polling()
