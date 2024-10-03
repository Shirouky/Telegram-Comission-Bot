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
        crud.delete_question(db=next(get_db()), question_id=message.reply_to_message.id)
    else:
        text = crud.get_text(db=next(get_db()), callback_text=["error_reply"])
        bot.send_message(message.chat.id, text["error_reply"], reply_to_message_id=message.id)


@bot.message_handler(content_types=["text", "photo"])
def show_menu(message, user_id=False):
    chat_id = message.chat.id
    text_menu = crud.get_text(db=next(get_db()), callback_text=["text_menu"])
    if user_id or message.text == text_menu["text_menu"] and chat_id != admin_chat_id:
        if not user_id:
            user_id = message.from_user.id
        text = crud.open_menu(db=next(get_db()), user_id=user_id, chat_id=chat_id)
        text_menu_ask = text["text_menu_ask"]
        del text["text_menu_ask"]
        keys = []
        buttons = list(text.keys())
        for button in buttons:
            title = text[button]
            keys.append([types.InlineKeyboardButton(title, callback_data=button)])
        keyboard = types.InlineKeyboardMarkup(keys)

        bot.send_message(chat_id, text_menu_ask, reply_markup=keyboard)

    elif message.reply_to_message and chat_id == admin_chat_id:
        question = crud.answer_question(db=next(get_db()), message=message)
        bot.copy_message(question["chat_id"], admin_chat_id, message.id, reply_to_message_id=question["message_id"])

    elif chat_id != admin_chat_id:
        text = crud.get_text(db=next(get_db()), callback_text=["error_text"])
        bot.send_message(chat_id, text["error_text"], reply_to_message_id=message.id)


@bot.callback_query_handler(func=lambda call: True)
def press_buttons(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    title = call.data[7:]
    message = call.message
    bot.delete_message(chat_id, message.id)
    match title:
        case "question" | "phones":
            ask_info(call, request=title)
        case "map":
            show_map(user_id=user_id, chat_id=chat_id)
        case "back":
            faq(user_id=user_id, chat_id=chat_id)
        case "years":
            show_years(user_id=user_id, chat_id=chat_id)
        case "news_subscribed" | "news_unsubscribed":
            text = crud.change_subscribe(db=next(get_db()), user_id=user_id, chat_id=chat_id)
            bot.send_message(chat_id, text["text_" + title], parse_mode="HTML")
        case "faq":
            faq(user_id=user_id, chat_id=chat_id)
        case "menu":
            show_menu(message, user_id)
        case "program":
            faq_program(user_id=user_id, chat_id=chat_id)
        case "bi":
            faq_bi(user_id=user_id, chat_id=chat_id)
        case "sa":
            faq_sa(user_id=user_id, chat_id=chat_id)
        case "faculty" | "vsb" | "work" | "dorm" | "exams" | "other":
            text_callback = "text" + title[6:]
            text = crud.get_button_text(db=next(get_db()), callback=text_callback, user_id=user_id, chat_id=chat_id)
            send_text(chat_id, text, text_callback, "button_faq")
        case "bi_ii" | "bi_ce" | "bi_work" | "bi_vsb" | "bi_more":
            text_callback = "text" + title[6:]
            text = crud.get_button_text(db=next(get_db()), callback=text_callback, user_id=user_id, chat_id=chat_id)
            send_text(chat_id, text, text_callback, "button_bi")
        case "sa_prog" | "sa_work" | "sa_vsb" | "sa_more":
            text_callback = "text" + title[6:]
            text = crud.get_button_text(db=next(get_db()), callback=text_callback, user_id=user_id, chat_id=chat_id)
            send_text(chat_id, text, text_callback, "button_sa")


def send_text(chat_id: int, text: dict, text_callback: str, callback: str):
    keys = [[types.InlineKeyboardButton(text["button_back"], callback_data=callback)]]
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(chat_id, text[text_callback], parse_mode="HTML", reply_markup=keyboard)


def faq(user_id: int, chat_id: int):
    text = crud.open_faq(db=next(get_db()), user_id=user_id, chat_id=chat_id)
    text_faq_ask = text["text_faq_ask"]
    keys = [[types.InlineKeyboardButton(text["button_faculty"], callback_data="button_faculty"),
             types.InlineKeyboardButton(text["button_program"], callback_data="button_program")]]
    buttons = list(text.keys())[3:]
    for button in buttons:
        title = text[button]
        keys.append([types.InlineKeyboardButton(title, callback_data=button)])
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(chat_id, text_faq_ask, reply_markup=keyboard)


def faq_program(user_id: int, chat_id: int):
    keys = []
    text = crud.open_faq_program(db=next(get_db()), user_id=user_id, chat_id=chat_id)
    text_program_ask = text["text_program_ask"]
    buttons = list(text.keys())[1:]
    for button in buttons:
        title = text[button]
        keys.append([types.InlineKeyboardButton(title, callback_data=button)])
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(chat_id, text_program_ask, reply_markup=keyboard)


def faq_bi(user_id: int, chat_id: int):
    keys = []
    text = crud.open_faq_bi(db=next(get_db()), user_id=user_id, chat_id=chat_id)
    text_program_ask = text["text_bi_sa_ask"]
    buttons = list(text.keys())[1:]
    for button in buttons:
        title = text[button]
        keys.append([types.InlineKeyboardButton(title, callback_data=button)])
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(chat_id, text_program_ask, reply_markup=keyboard)


def faq_sa(user_id: int, chat_id: int):
    keys = []
    text = crud.open_faq_sa(db=next(get_db()), user_id=user_id, chat_id=chat_id)
    text_program_ask = text["text_bi_sa_ask"]
    buttons = list(text.keys())[1:]
    for button in buttons:
        title = text[button]
        keys.append([types.InlineKeyboardButton(title, callback_data=button)])
    keyboard = types.InlineKeyboardMarkup(keys)
    bot.send_message(chat_id, text_program_ask, reply_markup=keyboard)


def ask_info(call, request):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    title = "text_" + request + "_ask"
    text = crud.ask_info(db=next(get_db()), user_id=user_id, chat_id=chat_id, title=title)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text["button_back"]))
    bot.send_message(chat_id, text[title], reply_markup=markup)
    bot.register_next_step_handler(call.message, get_info, request, text["button_back"])


def get_info(message, request, button_back):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if message.text != button_back:
        request_data = {"user_message_id": message.id}
        if request == "question":
            if message.content_type == "text":
                request_data["text"] = message.text
                request_data["has_photo"] = False
            else:
                request_data["text"] = message.caption
                request_data["has_photo"] = True

            admin_message = bot.forward_message(admin_chat_id, message.chat.id, message.id)
            request_data["admin_message_id"] = admin_message.id
            text = crud.save_question(db=next(get_db()), user_id=user_id, chat_id=chat_id, **request_data)

            bot.reply_to(admin_message, text["text_admin_question"])
            bot.pin_chat_message(admin_chat_id, admin_message.id, disable_notification=True)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(text["text_menu"]))
            bot.send_message(message.chat.id, text["text_question_thanks"], reply_markup=markup)
        else:
            admin_message = bot.forward_message(admin_chat_id, message.chat.id, message.id)
            text = crud.save_phone(db=next(get_db()), **request_data)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(text["text_menu"]))

            bot.send_message(message.chat.id, text["text_phone_thanks"], reply_markup=markup)

            bot.reply_to(admin_message, text["text_admin_phone"])
            bot.pin_chat_message(admin_chat_id, admin_message.id, disable_notification=True)
            request_data["admin_message_id"] = message.text

    else:
        show_menu(message, user_id)


def show_map(user_id: int, chat_id: int):
    with open("map.png", "rb") as photo:
        text = crud.show_map(db=next(get_db()), user_id=user_id, chat_id=chat_id)
        keys = [[types.InlineKeyboardButton(text["text_back"], callback_data="button_menu")]]
        keyboard = types.InlineKeyboardMarkup(keys)
        bot.send_photo(chat_id, photo, caption=text["text_map"], parse_mode="HTML",
                       reply_markup=keyboard)


def show_years(user_id: int, chat_id: int):
    with open("years.jpg", "rb") as photo:
        text = crud.show_years(db=next(get_db()), user_id=user_id, chat_id=chat_id)
        keys = [[types.InlineKeyboardButton(text["text_back"], callback_data="button_faq")]]
        keyboard = types.InlineKeyboardMarkup(keys)
        bot.send_photo(chat_id, photo, caption=text["text_years"], parse_mode="HTML",
                       reply_markup=keyboard)


bot.infinity_polling()
