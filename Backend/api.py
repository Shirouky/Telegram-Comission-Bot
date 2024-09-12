from crud import *
from models_orm import Base

from uvicorn import run
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


engine = create_engine('sqlite:///database.db', echo=False)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)

app = FastAPI()


@app.get("/user/{user_id}", response_model=UserModel)
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id=user_id)


@app.post("/users/", response_model=UserModel)
def create_user_route(user: BaseUser, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@app.get("/message/{message_id}", response_model=MessageModel)
def read_post_route(message_id: int, db: Session = Depends(get_db)):
    return get_message(db, message_id=message_id)


@app.post("/messages/", response_model=MessageModel)
def create_post_route(message: BaseMessage, db: Session = Depends(get_db)):
    return create_message(db=db, message=message)


@app.post("/text/", response_model=GetText)
def read_text_route(callback_text: GetTextModel, db: Session = Depends(get_db)):
    return get_text(db, callback_text=callback_text)


@app.post("/texts/", response_model=TextModel)
def create_post_route(text: BaseText, db: Session = Depends(get_db)):
    return create_text(db=db, text=text)


@app.get("/question/{question_id}", response_model=QuestionModel)
def read_question_route(question_id: int, db: Session = Depends(get_db)):
    return get_question(db, question_id=question_id)


@app.post("/questions/", response_model=QuestionModel)
def create_question_route(question: BaseQuestion, db: Session = Depends(get_db)):
    return create_question(db=db, question=question)


@app.patch("/questions/", response_model=QuestionModel)
def answer_question_route(data: AnswerModel, db: Session = Depends(get_db)):
    return answer_question(db=db, data=data)


@app.delete("/questions/", response_model=QuestionModel)
def delete_question_route(question_id: int, db: Session = Depends(get_db)):
    return delete_question(db=db, question_id=question_id)


@app.get("/phone/{phone_id}", response_model=PhoneModel)
def read_phone_route(phone_id: int, db: Session = Depends(get_db)):
    return get_phone(db, phone_id=phone_id)


@app.post("/phones/", response_model=PhoneModel)
def create_phone_route(phone: BasePhone, db: Session = Depends(get_db)):
    return create_phone(db=db, phone=phone)


@app.delete("/phones/", response_model=PhoneModel)
def answer_phone_route(phone_id: int, db: Session = Depends(get_db)):
    return answer_phone(db=db, phone_id=phone_id)


@app.get("/notification/{notification_id}", response_model=NotificationModel)
def read_notification_route(notification_id: int, db: Session = Depends(get_db)):
    return get_notification(db, notification_id=notification_id)


@app.post("/notifications/", response_model=List[int])
def create_notification_route(notification: BaseNotification, db: Session = Depends(get_db)):
    create_notification(db=db, notification=notification)
    return get_subscribers(db=db)


@app.get("/action/{action_id}", response_model=ActionModel)
def read_action_route(action_id: int, db: Session = Depends(get_db)):
    return get_action(db, action_id=action_id)


@app.post("/actions/", response_model=ActionModel)
def create_notification_route(action: BaseAction, db: Session = Depends(get_db)):
    return create_action(db=db, action=action)


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)
