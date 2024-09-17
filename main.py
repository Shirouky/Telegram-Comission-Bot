import crud
from models_api import *

from telebot import TeleBot, types
from json import load, dump
from models_orm import Base

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

with open("database.json", 'r') as database:
    data = load(database)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


engine = create_engine('sqlite:///database.db', echo=False)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)

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
    text = crud.start(db=next(get_db()), message=message)
    if message.chat.id != admin_chat_id:
        markup.add(types.KeyboardButton(text["text_menu"]))
    bot.send_message(message.chat.id, text["text_hello"], reply_markup=markup, parse_mode="HTML")


@bot.message_handler(commands=["news"])
def create_news(message):
    ids = create_notification({"message_id": message.reply_to_message.id, "admin_id": message.from_user.id,
                               "text": message.reply_to_message.text})
    for id_ in ids:
        bot.copy_message(id_, admin_chat_id, message.reply_to_message.id)
    text_ = get_text("admin_message_news")
    # for id_ in data["news"]:
    #     bot.copy_message(id_, admin_chat_id, message.reply_to_message.id)
    # bot.send_message(admin_chat_id, text["admin_messages"]["news"])


@bot.message_handler(commands=["delete"])
def delete_question(message):
    if message.reply_to_message and message.chat.id == admin_chat_id:
        remove_from_db(message, "questions")
        remove_from_db(message, "phones")
    else:
        bot.send_message(message.chat.id, text["errors"]["reply"])


@bot.message_handler(content_types=["text", "photo"])
def show_menu(message):
    text_menu = crud.get_text(db=next(get_db()), callback_text=["text_menu"])
    if message.text == text_menu["text_menu"] and message.chat.id != admin_chat_id:
        text = crud.open_menu(db=next(get_db()), message=message)
        text_menu_ask = text["text_menu_ask"]
        del text["text_menu_ask"]
        keys = []
        buttons = list(text.keys())
        for button in buttons:
            title = text[button]
            keys.append([types.InlineKeyboardButton(title, callback_data=button)])
        keyboard = types.InlineKeyboardMarkup(keys)

        bot.send_message(message.chat.id, text_menu_ask, reply_markup=keyboard)

    elif message.reply_to_message and message.chat.id == admin_chat_id:
        question = crud.answer_question(db=next(get_db()), message=message)
        bot.copy_message(question["chat_id"], admin_chat_id, message.id, reply_to_message_id=question["message_id"])

    elif message.chat.id != admin_chat_id:
        text = crud.get_text(db=next(get_db()), callback_text=["error_text"])
        bot.send_message(message.chat.id, text["error_text"], reply_to_message_id=message.id)


@bot.callback_query_handler(func=lambda call: True)
def press_buttons(call):
    message = call.message
    chat_id = call.message.chat.id
    user_id = call.message.from_user.id
    title = call.data
    # action = BaseAction(title=title, user_id=user_id, chat_id=chat_id)
    # crud.create_action(db=next(get_db()), action=action)
    match call.data:
        case "questions" | "phones":
            ask_info(message, call.data)
        case "map":
            show_map(message)
        case "years":
            show_years(message)
        case "addnews" | "removenews":
            crud.change_subscribe(db=next(get_db()), user_id=user_id)
            change_news(message)
        case "faq":
            bot.delete_message(chat_id, message.id)
            faq(message)
        case "program":
            bot.delete_message(chat_id, message.id)
            faq_program(message)
        case "bi" | "sa":
            bot.delete_message(chat_id, message.id)
            faq_bi_sa(call.message, call.data)
        case "faculty" | "vsb" | "work" | "dorm" | "exams" | "other":
            bot.delete_message(chat_id, message.id)
            send_text(call.message, text["faq"][call.data]["text"], "faq")
        case "bi_ii" | "bi_ce" | "work_bi" | "vsb_bi" | "more_bi":
            bot.delete_message(chat_id, message.id)
            send_text(call.message, text["faq"]["program"]["bi"][call.data]["text"], "bi")
        case "sa_prog" | "work_sa" | "vsb_sa" | "more_sa":
            bot.delete_message(chat_id, message.id)
            send_text(call.message, text["faq"]["program"]["sa"][call.data]["text"], "sa")


def send_text(message, button_text, callback):
    text = crud.get_text(db=next(get_db()), callback_text=["text_back"])
    keys = [[types.InlineKeyboardButton(text["text_back"], callback_data=callback)]]
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(message.chat.id, button_text, parse_mode="HTML", reply_markup=keyboard)


def faq(message):
    text = crud.faq(db=next(get_db()), message=message)
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

        bot.send_message(admin_chat_id, text["admin_messages"][request])
        admin_message = bot.forward_message(admin_chat_id, message.chat.id, message.id)
        bot.pin_chat_message(admin_chat_id, admin_message.id, disable_notification=True)

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
        bot.send_photo(message.chat.id, photo, caption=text["faq"]["years"]["text"], parse_mode="HTML",
                       reply_markup=keyboard)


def change_news(message):
    update_db()
    subscribe = str(message.chat.id in data["news"])
    bot.send_message(message.chat.id, text["news_buttons"][subscribe]["text"])


def update_db():
    with open("database.json", "w") as f:
        dump(data, f)


def remove_from_db(message, title):
    for elem in data[title]:
        if message.reply_to_message.id == elem["admin_chat_message_id"]:
            bot.unpin_chat_message(admin_chat_id, message.reply_to_message.id)
            data[title].remove(elem)
            update_db()
            return elem


bot.infinity_polling()
