from crud import create_text
from models_api import BaseText
from models_orm import Base
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

texts = []
texts.append(BaseText(callback_text="text_hello",
                      text="Привет! Это бот команды приемной комиссии ФБИУКС. <i>Здесь Вы можете узнать ответы на все свои вопросы</i> ☺️"))
texts.append(BaseText(callback_text="text_back", text="🔙 Назад"))
texts.append(BaseText(callback_text="text_menu", text="\uD83D\uDD06 Открыть меню"))
texts.append(BaseText(callback_text="text_menu_ask", text="Что будем делать?"))
texts.append(BaseText(callback_text="button_faculty", text="⚛️ Факультет"))
texts.append(BaseText(callback_text="button_program", text="📔 Программы"))
texts.append(BaseText(callback_text="button_years", text="📝 Проходные баллы прошлых лет"))
texts.append(BaseText(callback_text="button_vsb", text="📑 Временный студенческий билет"))
texts.append(BaseText(callback_text="button_work", text="💼 Трудоустройство"))
texts.append(BaseText(callback_text="button_dorm", text="🏢 Общежитие"))
texts.append(BaseText(callback_text="button_exams", text="🎟️ Внутренние экзамены"))
texts.append(BaseText(callback_text="button_other", text="\uD83D\uDCAC Другое"))
texts.append(BaseText(callback_text="button_news_subscribed", text="📩 Отписаться от рассылки"))
texts.append(BaseText(callback_text="button_news_unsubscribed", text="💌 Подписаться на рассылку"))
texts.append(BaseText(callback_text="error_text", text="❌ Выберите, что хотите сделать, из меню"))
texts.append(BaseText(callback_text="error_reply", text="❌ Эта команда должна быть использована в ответ на сообщение"))
texts.append(BaseText(callback_text="text_admin_news", text="Новость разослана всем абитуриентам"))
texts.append(BaseText(callback_text="text_admin_question", text="❗ Новый вопрос ❗"))
texts.append(BaseText(callback_text="text_admin_phone", text="❗ Новая заявка на звонок ❗"))
texts.append(BaseText(callback_text="button_faq", text="❓ Частые вопросы ❓"))
texts.append(BaseText(callback_text="button_question", text="❔ Задать свой вопрос"))
texts.append(BaseText(callback_text="button_phone", text="📞 Запросить звонок"))
texts.append(BaseText(callback_text="button_map", text="🗺️ Как до нас добраться?"))
texts.append(BaseText(callback_text="text_question_ask",
                      text="❓ Задайте интересующий вопрос. Он будет отправлен администраторам. Позже с Вами свяжутся (если у Вас скрыт аккаунт, напишите, как с Вами связаться)"))
texts.append(BaseText(callback_text="text_phone_ask", text="Напишите свой номер телефона"))
texts.append(
    BaseText(callback_text="text_question_thanks", text="❤️ Спасибо за вопрос! Скоро администраторы ответят на него"))
texts.append(BaseText(callback_text="text_phone_thanks", text="❤️ С Вами свяжутся в ближайшее время"))

texts.append(BaseText(callback_text="text_map", text="Каширское ш., д. 31, корпус Б, кабинет 214. <b>Чтобы попасть на территорию университета нужно зарегистрироваться на проходной (слева) и предъявить паспорт. Не забудьте взять его с собой!</b>"))
texts.append(BaseText(callback_text="text_bi_sa_ask", text="❓ Что Вы хотите узнать?"))
texts.append(BaseText(callback_text="text_faq_ask", text="❓ Здесь можно узнать больше про ФБИУКС. Что Вас интересует?"))
texts.append(BaseText(callback_text="text_program_ask", text="❓ Про какое направление Вы хотите узнать?"))

for text in texts:
    print(text.callback_text)
    text.text = text.text.encode('raw_unicode_escape').decode('unicode_escape').encode('utf-16_BE','surrogatepass').decode('utf-16_BE')
    create_text(db=next(get_db()), text=text)
