from sqlalchemy.orm import Session
from models_orm import User, Message, BotText, Question, Action, Phone, Notification
from models_api import *


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def get_subscribers(db: Session):
    return db.query(User).filter(User.subscribed).all()


def change_subscribe(db: Session, user_id: int):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    db_user.subscribe = not db_user.subscribe
    db.commit()
    db.refresh(db_user)
    return db_user


def check_subscribe(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first().subscribe


def create_user(db: Session, user):
    db_user = User(user_id=user.user_id, username=user.username, is_premium=user.is_premium,
                   date_started=datetime.now())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()


def create_message(db: Session, message: BaseMessage):
    db_message = Message(message_id=message.message_id,
                         user_id=message.user_id, date=datetime.now(), text=message.text,
                         user_type=message.user_type)

    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_text(db: Session, callback_text):
    texts = {}
    for call in callback_text:
        text = db.query(BotText).filter(BotText.callback_text == call).first()
        texts[call] = text.text
    return texts


def start(db: Session, message):
    user_id = message.from_user.id
    user = BaseUser(user_id=user_id, username=message.from_user.username, chat_id=message.chat.id,
                    is_premium=message.from_user.is_premium != None)
    create_user(db=db, user=user)
    action = BaseAction(title="start", user_id=message.from_user.id, chat_id=message.chat.id)
    create_action(db=db, action=action)
    return get_text(db=db, callback_text=["text_menu", "text_hello"])


def faq(db: Session, message):
    action = BaseAction(title="open faq", user_id=message.from_user.id, chat_id=message.chat.id)
    create_action(db=db, action=action)
    return get_text(db=db, callback_text=["text_menu", "text_hello"])


def open_menu(db: Session, message):
    user_id = message.from_user.id
    action = BaseAction(title="open menu", user_id=user_id, chat_id=message.chat.id)
    create_action(db=db, action=action)
    text = ["text_menu_ask", "button_question", "button_phone", "button_map"]
    if user_is_subscribed(db=db, user_id=user_id):
        text.append("button_news_subscribed")
    else:
        text.append("button_news_unsubscribed")
    return get_text(db=db, callback_text=text)


def open_faq(db: Session, message):
    user_id = message.from_user.id
    action = BaseAction(title="open faq", user_id=user_id, chat_id=message.chat.id)
    create_action(db=db, action=action)
    text = ["text_faq_ask", "button_faculty", "button_program", "button_years", "button_vsb", "button_work",
            "button_dorm",
            "button_exams", "button_other"]
    return get_text(db=db, callback_text=text)


def user_is_subscribed(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first().subscribed


def create_text(db: Session, text: BaseText):
    db_text = BotText(text=text.text, callback_text=text.callback_text)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text


def get_question(db: Session, question_id: int):
    return db.query(Question).filter(Question.admin_message_id == question_id).first()


def create_question(db: Session, question: BaseQuestion):
    db_question = Question(text=question.text, date_added=datetime.now(), has_photo=question.has_photo,
                           user_chat_id=question.user_chat_id, user_message_id=question.user_message_id,
                           user_id=question.user_id, admin_message_id=question.admin_message_id)

    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def answer_question(db: Session, message):
    db_question = get_question(db=db, question_id=message.reply_to_message.id)
    db_question.answer_text = message.text
    db_question.answer_id = message.id
    db_question.date_answered = datetime.now()
    db_question.admin_id = message.from_user.id
    db_question.admin_has_photo = message.type == "photo"
    db.commit()
    db.refresh(db_question)
    response = {"chat_id": db_question.user_chat_id, "message_id": db_question.user_message_id}
    return response


def delete_question(db: Session, question_id: int):
    db_question = get_question(db=db, question_id=question_id)
    db_question.is_deleted = True
    db.commit()
    db.refresh(db_question)
    return db_question


def get_phone(db: Session, phone_id: int):
    return db.query(Phone).filter(Phone.id == phone_id).first()


def create_phone(db: Session, phone: BasePhone):
    db_phone = Phone(phone=phone.phone, date_added=datetime.now(), user_chat_id=phone.user_chat_id,
                     user_message_id=phone.message_id, user_id=phone.user_id)

    db.add(db_phone)
    db.commit()
    db.refresh(db_phone)
    return db_phone


def answer_phone(db: Session, phone_id: int):
    db_phone = get_phone(db=db, phone_id=phone_id)
    db_phone.is_answered = True
    db.commit()
    db.refresh(db_phone)
    return db_phone


def get_action(db: Session, action_id: int):
    return db.query(Action).filter(Action.id == action_id).first()


def create_action(db: Session, action: BaseAction):
    db_action = Action(user_id=action.user_id, chat_id=action.chat_id, date=datetime.now(), title=action.title)

    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action


def get_notification(db: Session, notification_id: int):
    return db.query(Notification).filter(Notification.id == notification_id).first()


def create_notification(db: Session, notification: BaseNotification):
    db_notification = Notification(message_id=notification.message_id, text=notification.type,
                                   admin_id=notification.admin_id, date_posted=datetime.now())

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
