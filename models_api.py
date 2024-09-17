from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BaseUser(BaseModel):
    user_id: int
    chat_id: int
    username: str
    is_premium: bool

    questions: List = None
    actions: List = None

    class Config:
        from_attributes = True


class UserModel(BaseUser):
    id: int
    date_started: datetime


class BaseMessage(BaseModel):
    message_id: int
    user_id: int
    text: str
    user_type: str

    class Config:
        from_attributes = True


class MessageModel(BaseMessage):
    id: int
    date: datetime


class BaseText(BaseModel):
    text: str
    callback_text: str

    class Config:
        from_attributes = True


class TextModel(BaseText):
    id: int


class GetText(BaseModel):
    data: dict


class BaseQuestion(BaseModel):
    user_id: int
    user_chat_id: int
    user_message_id: int
    admin_message_id: int
    text: str
    has_photo: bool

    class Config:
        from_attributes = True


class QuestionModel(BaseQuestion):
    id: int
    answer_text: Optional[str]
    answer_id: Optional[int]
    date_added: datetime
    date_answered: Optional[datetime]
    admin_id: Optional[int]
    is_deleted: bool
    admin_has_photo: Optional[bool]


class AnswerModel(BaseModel):
    admin_message_id: int
    answer_text: str
    answer_id: int
    admin_id: int
    admin_has_photo: bool


class BasePhone(BaseModel):
    user_id: int
    user_chat_id: int
    user_message_id: int
    admin_message_id: int
    phone: str

    class Config:
        from_attributes = True


class PhoneModel(BasePhone):
    id: int
    date_added: datetime
    date_answered: Optional[datetime]
    admin_id: Optional[int]
    is_answered: bool


class BaseAction(BaseModel):
    user_id: int
    chat_id: int
    title: str

    class Config:
        from_attributes = True


class ActionModel(BaseAction):
    id: int
    date: datetime


class BaseNotification(BaseModel):
    message_id: int
    admin_id: int
    text: str

    class Config:
        from_attributes = True


class NotificationModel(BaseNotification):
    id: int
    date_posted: datetime


class GetTextModel(BaseModel):
    data: List