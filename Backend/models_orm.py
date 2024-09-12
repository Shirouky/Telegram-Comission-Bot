from sqlalchemy import Column, Integer, Text, Table, DateTime, Boolean, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    date_started = Column(DateTime)
    is_premium = Column(Boolean, default=False)
    subscribed = Column(Boolean, default=False)

    # questions_admins = relationship("Question", backref="user_questions", cascade="all,delete,save-update")
    # questions_users = relationship("Question", backref="admin_questions", cascade="all,delete,save-update")

    actions = relationship("Action", backref="user_actions", cascade="all,delete,save-update")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message_id = Column(Integer)
    text = Column(Text)
    date = Column(DateTime)
    user_type = Column(String)

    def __repr__(self):
        return "<User('%s', '%s', '%s', '%s', '%s', '%s')>" % (
            self.id, self.user_id, self.username, self.text, self.date, self.from_user)


class BotText(Base):
    __tablename__ = 'texts'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    callback_text = Column(String)

    def __repr__(self):
        return "<Text('%s', '%s', '%s')>" % (
            self.id, self.text, self.callback_text)


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    answer_text = Column(Text)
    answer_id = Column(Integer)
    date_added = Column(DateTime)
    date_answered = Column(DateTime, default=datetime.min)

    user_chat_id = Column(Integer)
    user_message_id = Column(Integer)
    admin_message_id = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    admin_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", foreign_keys=[user_id])
    admins = relationship("User", foreign_keys=[admin_id])

    is_deleted = Column(Boolean, default=False)
    has_photo = Column(Boolean)
    admin_has_photo = Column(Boolean)

    @property
    def __repr__(self):
        return "<Question('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
            self.id, self.text, self.answer_text, self.answer_id, self.date_added, self.date_answered,
            self.user_chat_id, self.user_message_id, self.user_id, self.admin_id, self.username, self.admin_name,
            self.is_deleted, self.has_photo)


class Phone(Base):
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True)
    number = Column(Text)
    is_answered = Column(Boolean, default=False)
    date_added = Column(DateTime)
    date_answered = Column(DateTime, default=datetime.min)
    user_chat_id = Column(Integer)
    admin_message_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    admin_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", foreign_keys=[user_id])
    admins = relationship("User", foreign_keys=[admin_id])

    def __repr__(self):
        return "<Phone('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
            self.id, self.number, self.is_answered, self.date_added, self.date_answered, self.user_chat_id,
            self.user_id, self.admin_id)


class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    chat_id = Column(Integer)

    def __repr__(self):
        return "<Action('%s', '%s', '%s', '%s')>" % (
            self.id, self.title, self.date, self.user_id)


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    message_id = Column(Integer)
    date_posted = Column(DateTime)

    admin_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return "<Notification('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
            self.id, self.message_id, self.text, self.is_posted, self.date_added, self.date_posted, self.admin_id,
            self.users)
