from telebot import TeleBot, types
import json

with open("database.json", "r") as f:
    json_object = json.load(f)


bot = TeleBot(json_object['token'])  # bot's token
admin_chat_id = json_object['admin_chat_id']

bot.set_my_commands(
    commands=[
        types.BotCommand('update', 'Обновить FAQ'),
    ],
    scope=types.BotCommandScopeChat(admin_chat_id)
)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Это бот команды приемной комиссии ФБИУКС. *Здесь ты можешь узнать ответы на все свои вопросы*☺️📎", parse_mode= 'Markdown')
    show_menu(message)


@bot.message_handler(commands=['menu'])
def show_menu(message):
    keys = [[types.InlineKeyboardButton('FAQ', callback_data='faq')],
            [types.InlineKeyboardButton('Задать свой вопрос', callback_data='question')],
            [types.InlineKeyboardButton('Заказать звонок', callback_data='phone')],
            [types.InlineKeyboardButton('Как до нас добраться?', callback_data='map')]]
    keyboard = types.InlineKeyboardMarkup(keys)

    bot.send_message(message.chat.id, 'Что будем делать?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def press_buttons(call):
    if call.data == 'faq':
        faq(call.message)
    elif call.data == 'question':
        ask_question(call.message)
    elif call.data == 'phone':
        phone(call.message)
    elif call.data == 'map':
        show_map(call.message)


def faq(message):
    bot.copy_message(message.chat.id, admin_chat_id, json_object['faq_message_id'])


@bot.message_handler(commands=['update'])
def update_faq(message):
    if message.reply_to_message:
        bot.send_message(admin_chat_id,
                         "FAQ обновлены")
        json_object['faq_message_id'] = message.reply_to_message.id
        with open("database.json", "w") as f:
            f.write(json_object)
    else:
        bot.send_message(admin_chat_id, 'Эта команда должна быть использована в ответ на сообщение')


def ask_question(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, '❓ Задайте интересующий вопрос. Он будет отправлен администраторам. Позже с Вами свяжутся (если у Вас скрыт аккаунт, напишите, как с Вами связаться)',
                     reply_markup=markup)
    bot.register_next_step_handler(message, get_question)


def get_question(message):
    bot.send_message(message.chat.id, 'Спасибо за вопрос!')
    show_menu(message)
    bot.send_message(admin_chat_id, '❗ Новый вопрос ❗')
    bot.forward_message(admin_chat_id, message.chat.id, message.id)


def phone(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Напишите свой номер телефона',
                     reply_markup=markup)
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'С Вами свяжутся в ближайшее время',
                     reply_markup=markup)
    show_menu(message)
    bot.send_message(admin_chat_id, '❗ Новая заявка на звонок ❗')
    bot.forward_message(admin_chat_id, message.chat.id, message.id)


def show_map(message):
    bot.send_message(message.chat.id,
                     'Каширское ш., д. 31, корпус Б, кабинет 214',
                     parse_mode='Markdown')
    photo = open("map.png", 'rb')
    bot.send_photo(message.chat.id, photo)
    photo.close()
    show_menu(message)


bot.infinity_polling()
