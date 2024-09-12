from sys import path

path.append("../Backend")

from models_api import BaseUser, GetTextModel, BaseMessage, BaseQuestion, BaseAction, BaseNotification

from requests import get, patch, post
from json import loads

link = "http://127.0.0.1:8000/"


def get_user(user_id: int):
    return loads(get(link + f"user/{user_id}").text)


def create_user(user: BaseUser):
    return post(link + "users", json=user)


def get_message(message_id: int):
    return loads(get(link + f"message/{message_id}").text)


def create_message(message: BaseMessage):
    return post(link + "messages", json=message)


def get_text(callback_text: GetTextModel):
    return post(link + f"text/", json=callback_text)


def get_question(question_id: int):
    return loads(get(link + f"question/{question_id}").text)


def create_question(question: BaseQuestion):
    return post(link + "questions", json=question)


def get_notification(notification_id: int):
    return loads(get(link + f"notification/{notification_id}").text)


def create_notification(notification: BaseNotification):
    return post(link + "notifications", json=notification)


# def get_action(action_id: int):
#     return loads(get(link + f"action/{action_id}").text)


def create_action(action: BaseAction):
    return post(link + "actions", json=action)
