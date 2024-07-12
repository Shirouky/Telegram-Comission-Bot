from telebot import TeleBot, types
from json import load, dump
import text

with open("database.json", "r") as f:
    json_object = load(f)

bot = TeleBot(json_object["bot_data"]["token"])
admin_chat_id = json_object["bot_data"]["admin_chat_id"]

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
    markup.add(types.KeyboardButton("Открыть меню"))
    bot.send_message(message.chat.id, text.hello, parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(commands=["news"])
def create_news(message):
    for id_ in json_object["news"]:
        bot.copy_message(id_, admin_chat_id, message.reply_to_message.id)
    bot.send_message(admin_chat_id, "Новость разослана всем абитуриентам")


@bot.message_handler(commands=["delete"])
def delete_question(message):
    if message.reply_to_message and message.chat.id == admin_chat_id:
        answered = False
        questions = json_object["questions"]
        for question in questions:
            if message.reply_to_message.id == question["in_admin_message_id"]:
                answered = True
                bot.unpin_chat_message(admin_chat_id, message.reply_to_message.id)
                questions.remove(question)
                json_object["questions"] = questions
                with open("database.json", "w") as f:
                    dump(json_object, f)

        if not answered:
            phones = json_object["phones"]
            for phone in phones:
                if message.reply_to_message.id == phone["in_admin_message_id"]:
                    bot.unpin_chat_message(admin_chat_id, message.reply_to_message.id)
                    phones.remove(phone)
                    json_object["phones"] = phones
                    with open("database.json", "w") as f:
                        dump(json_object, f)
    else:
        bot.send_message(message.chat.id,
                         "Эта команда должна быть использована в ответ на сообщение", parse_mode="Markdown")


@bot.message_handler(content_types=["text"])
def show_menu(message):
    if message.text == "Открыть меню":
        news = which_button(message.chat.id)
        keys = [[types.InlineKeyboardButton("❓ FAQ ❓", callback_data="faq")],
                [types.InlineKeyboardButton("❔ Задать свой вопрос", callback_data="question")],
                [types.InlineKeyboardButton("📞 Запросить звонок", callback_data="phone")],
                [types.InlineKeyboardButton("🗺️ Как до нас добраться?", callback_data="map")],
                [types.InlineKeyboardButton(news[0], callback_data=news[1])]]
        keyboard = types.InlineKeyboardMarkup(keys)

        bot.send_message(message.chat.id, "Что будем делать?", reply_markup=keyboard)

    elif message.reply_to_message and message.chat.id == admin_chat_id:
        answered = False
        questions = json_object["questions"]
        for question in questions:
            if message.reply_to_message.id == question["in_admin_message_id"]:
                answered = True
                bot.unpin_chat_message(admin_chat_id, message.reply_to_message.id)
                bot.copy_message(question["chat_id"], admin_chat_id, message.id,
                                 reply_to_message_id=question["message_id"])
                questions.remove(question)
                json_object["questions"] = questions
                with open("database.json", "w") as f:
                    dump(json_object, f)

        if not answered:
            phones = json_object["phones"]
            for phone in phones:
                if message.reply_to_message.id == phone["in_admin_message_id"]:
                    bot.unpin_chat_message(admin_chat_id, message.reply_to_message.id)
                    phones.remove(phone)
                    json_object["phones"] = phones
                    with open("database.json", 'w') as f:
                        dump(json_object, f)


@bot.callback_query_handler(func=lambda call: True)
def press_buttons(call):
    match call.data:
        case "faq":
            faq(call.message)
        case "question":
            ask_question(call.message)
        case "phone":
            phone_func(call.message)
        case "map":
            show_map(call.message)
        case "addnews":
            add_news(call.message)
        case "removenews":
            remove_news(call.message)
        case "faculty":
            bot.send_message(call.message.chat.id, text.faculty, parse_mode="HTML")
        case "program":
            faq_program(call.message)
        case "vsb":
            bot.send_message(call.message.chat.id, text.vsb, parse_mode="HTML")
        case "exams":
            bot.send_message(call.message.chat.id, text.exams, parse_mode="HTML")
        case "dorm":
            bot.send_message(call.message.chat.id, text.dorm, parse_mode="HTML")
        case "work":
            bot.send_message(call.message.chat.id, text.work, parse_mode="HTML")
        case "bi":
            bot.send_message(call.message.chat.id, text.bi, parse_mode="HTML")
        case "sa":
            bot.send_message(call.message.chat.id, text.sa, parse_mode="HTML")
        case "other":
            bot.send_message(call.message.chat.id, text.other, parse_mode="HTML")


def faq(message):
    keys = [
        [types.InlineKeyboardButton("Факультет", callback_data="faculty"),
         types.InlineKeyboardButton("Программы", callback_data="program")],
        [types.InlineKeyboardButton("Временный студенческий билет", callback_data="vsb")],
        [types.InlineKeyboardButton("Вступительные экзамены", callback_data="exams")],
        [types.InlineKeyboardButton("Общежития", callback_data="dorm")],
        [types.InlineKeyboardButton("Трудоустройство", callback_data="work")],
        [types.InlineKeyboardButton("Другое", callback_data="alt")]]
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(message.chat.id, "Что Вы хотите узнать?", reply_markup=keyboard)


def faq_program(message):
    keys = [[types.InlineKeyboardButton("Бизнес-информатика", callback_data="bi")],
            [types.InlineKeyboardButton("Системный анализ", callback_data="sa")]]
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(message.chat.id, "Какое направление Вам интересно?", reply_markup=keyboard)


def ask_question(message):
    bot.send_message(message.chat.id, text.ask_question)
    bot.register_next_step_handler(message, get_question)


def get_question(message):
    bot.send_message(message.chat.id, text.thanks_question)
    if check_in_db(message):
        bot.send_message(admin_chat_id, "❗ Новый вопрос ❗")
        admin_message = bot.forward_message(admin_chat_id, message.chat.id, message.id)
        bot.pin_chat_message(admin_chat_id, admin_message.id, disable_notification=False)
        question = {"chat_id": message.chat.id, "message_id": message.id, "in_admin_message_id": admin_message.id}
        json_object["questions"].append(question)
        with open("database.json", "w") as f:
            dump(json_object, f)


def phone_func(message):
    bot.send_message(message.chat.id, "Напишите свой номер телефона")
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "С Вами свяжутся в ближайшее время",
                     reply_markup=markup)
    if check_in_db(message):
        bot.send_message(admin_chat_id, "❗ Новая заявка на звонок ❗")
        admin_message = bot.forward_message(admin_chat_id, message.chat.id, message.id)
        bot.pin_chat_message(admin_chat_id, admin_message.id, disable_notification=True)
        phone = {"chat_id": message.chat.id, "message_id": message.id, "in_admin_message_id": admin_message.id}
        json_object["phones"].append(phone)
        with open("database.json", "w") as f:
            dump(json_object, f)


def show_map(message):
    bot.send_message(message.chat.id, text.map, parse_mode="HTML")
    photo = open("map.png", "rb")
    bot.send_photo(message.chat.id, photo)
    photo.close()


def check_in_db(message):
    answered = False
    double = True
    questions = json_object["questions"]
    for question in questions:
        if message.chat.id == question["chat_id"] and message.id == question["message_id"]:
            answered = True
            double = True
            break

    if not answered:
        phones = json_object["phones"]
        for phone in phones:
            if message.chat.id == phone["chat_id"] and message.id == phone["message_id"]:
                double = True
                break
    return double


def which_button(chat_id):
    if chat_id not in json_object["news"]:
        return ["💌 Подписаться на рассылку", "addnews"]
    else:
        return ["📩 Отписаться от рассылки", "removenews"]


def add_news(message):
    json_object["news"].append(message.chat.id)
    with open("database.json", "w") as f:
        dump(json_object, f)
    bot.send_message(message.chat.id, "❤️ Вы успешно подписались на рассылку!")


def remove_news(message):
    json_object["news"].remove(message.chat.id)
    with open("database.json", "w") as f:
        dump(json_object, f)
    bot.send_message(message.chat.id, "💔 Вы отписались от рассылки")


bot.infinity_polling()
