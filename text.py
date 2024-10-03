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
                      text="Привет! Это бот команды приемной комиссии ФБИУКС.\n<i>Здесь Вы можете узнать ответы на все свои вопросы</i> ☺️"))
texts.append(BaseText(callback_text="button_back", text="🔙 Назад"))
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
texts.append(BaseText(callback_text="button_bi", text="Бизнес-информатика"))
texts.append(BaseText(callback_text="button_sa", text="⚙ Системный анализ"))
texts.append(BaseText(callback_text="button_map", text="🗺️ Как до нас добраться?"))
texts.append(BaseText(callback_text="text_question_ask",
                      text="❓ Задайте интересующий вопрос. Он будет отправлен администраторам. Позже с Вами свяжутся (если у Вас скрыт аккаунт, напишите, как с Вами связаться)"))
texts.append(BaseText(callback_text="text_phone_ask", text="Напишите свой номер телефона"))
texts.append(
    BaseText(callback_text="text_question_thanks", text="❤️ Спасибо за вопрос! Скоро администраторы ответят на него"))
texts.append(BaseText(callback_text="text_phone_thanks", text="❤️ С Вами свяжутся в ближайшее время"))

texts.append(BaseText(callback_text="text_map",
                      text="Каширское ш., д. 31, корпус Б, кабинет 214. <b>Чтобы попасть на территорию университета нужно зарегистрироваться на проходной (слева) и предъявить паспорт. Не забудьте взять его с собой!</b>"))
texts.append(BaseText(callback_text="text_bi_sa_ask", text="❓ Что Вы хотите узнать?"))
texts.append(BaseText(callback_text="text_faq_ask", text="❓ Здесь можно узнать больше про ФБИУКС. Что Вас интересует?"))
texts.append(BaseText(callback_text="text_program_ask", text="❓ Про какое направление Вы хотите узнать?"))

texts.append(BaseText(callback_text="button_bi_ce", text="🏦 Цифровая экономика"))
texts.append(BaseText(callback_text="text_bi_ce",
                      text="<b>«Бизнес-информатика в цифровой экономике»</b>\n\n\uD83C\uDFE6 Программа акцентируется на экономической стороне разработки и внедрения IT систем. \n\nДополнительные курсы, которых нет в программе «Искусственный интеллект и бизнес-информатика»:\n✔  Экономика организации (предприятия) (5 семестр) \n✔  Прогнозирование финансовых рынков (5 семестр) \n✔  Портфельное инвестирование (7 семестр) \n✔  Рынки информационных технологий и организации продаж (8 семестр)"))
texts.append(BaseText(callback_text="button_bi_ii", text="🤖 Искусственный интеллект"))
texts.append(BaseText(callback_text="text_bi_ii",
                      text="<b>«Искусственный интеллект и бизнес-информатика»</b>\n\n\uD83E\uDD16 Программа создана для подготовки специалистов в области внедрения методов машинного обучения и технологий искусственного интеллекта в организационные и бизнес-процессы, на уровне предприятий и государственных структур.\n\nДополнительные курсы, которых нет в программе «Бизнес-информатика в цифровой экономике»:\n✔  Теоретические основы искусственного интеллекта (5 семестр) \n✔  Методы искусственного интеллекта (5 семестр)\n✔  Психология саморазвития (6 семестр)\n✔  Приложение искусственного интеллекта в бизнес-информатике (7 семестр)\n✔  Инструменты искусственного интеллекта (low-code технологии) (8 семестр)"))
texts.append(BaseText(callback_text="button_sa", text="⚙ Системный анализ"))
texts.append(BaseText(callback_text="button_bi_vsb", text="\uD83D\uDCD1 Временный студенческий билет"))

texts.append(BaseText(callback_text="text_bi_vsb",
                      text="\uD83D\uDCAF С какими баллами выдают временный студенческий билет? 275+\n*<i>Баллы без учёта индивидуальных достижений</i>"))
texts.append(BaseText(callback_text="button_bi_work", text="💼 Трудоустройство"))
texts.append(BaseText(callback_text="text_bi_work",
                      text="<b>\uD83C\uDFA9 Профессии будущего</b>\n\n1️⃣ Разработчик моделей Big Data\n2️⃣ Архитектор информационных систем\n3️⃣ Криптовалютный трейдер\n4️⃣ Проектировщик-эргономист\n5️⃣ Оценщик интеллектуальной собственности\n6️⃣ Специалист по разработке и организации обучающих игр"))
texts.append(BaseText(callback_text="button_bi_more", text="💬 Узнать больше"))

texts.append(BaseText(callback_text="button_sa_program", text="⚙ Программа"))
texts.append(BaseText(callback_text="text_sa_program",
                      text="<b>«Системный анализ и управление жизненным циклом сложных систем»</b>\n\n⚙️ Программа направлена на подготовку профессионалов в области проектирования, разработки и управления информационными технологиями с помощью применения уникального комплекса методик в сферах системной инженерии и теории управления."))
texts.append(BaseText(callback_text="button_sa_vsb", text="\uD83D\uDCD1 Временный студенческий билет"))
texts.append(BaseText(callback_text="text_sa_vsb",
                      text="\uD83D\uDCAF С какими баллами выдают временный студенческий билет? 275+\n*<i>Баллы без учёта индивидуальных достижений</i>"))
texts.append(BaseText(callback_text="button_sa_work", text="💼 Трудоустройство"))
texts.append(BaseText(callback_text="text_work_sa",
                      text="<b>\uD83C\uDFA9 Профессии будущего</b>\n\n1️⃣ Системный аналитик \n2️⃣ Бизнес-аналитик \n3️⃣ Трендвотчер/Форсайтер\n4️⃣ Системный инженер интеллектуальных энергосетей\n5️⃣ Разработчик моделей Big Data\n6️⃣ Архитектор информационных систем"))
texts.append(BaseText(callback_text="button_sa_more", text="💬 Узнать больше"))
texts.append(BaseText(callback_text="text_sa_more",
                      text="\uD83D\uDCDA Узнать больше можно на официальном сайте ФБИУКС ▶️ <a href=\"https://bi.mephi.ru/bakalavriat/sa\">тык</a>"))

texts.append(BaseText(callback_text="text_years", text="\uD83D\uDCDD Проходные баллы прошлых лет на наши программы"))
texts.append(BaseText(callback_text="text_vsb",
                      text="\uD83D\uDCDD В чем смысл временного студенческого билета?\n\nЕсли Вы олимпиадник или высокобалльник и при этом не проходите по конкурсу на бюджет, то временный студенческий гарантирует зачисление на платное обучение за счёт средств университета. Оформить билет можно, подав оригинал документа об образовании.\n\n\uD83D\uDCAF С какими баллами выдают временный студенческий билет на ФБИУКС?\n\nБизнес-информатика: <b>275+</b>\nСистемный анализ: <b>275+</b>\n<i>*Баллы без учёта индивидуальных достижений</i>"))
texts.append(BaseText(callback_text="text_work",
                      text="\uD83D\uDCDC А что можете сказать про трудоустройство?\n\nУ Вас будут перспективы карьеры в следующих компаниях и организациях:\n<b>Экономика данных</b>: банки («Сбер», «Т-банк»), консалтинговые компании, финансовые структуры, а также «Яндекс», «Мейл ру», МТС\n<b>Высокотехнологичные предприятия</b>: предприятия Госкорпорации «Росатом», предприятия «Роскосмос»\n<b>Научные организации</b>: Институты Российской академии наук, Российские научные центры"))
texts.append(BaseText(callback_text="text_dorm",
                      text="\uD83C\uDFD8️ Какие в МИФИ общежития?\n\nЕсли Вы поступили на бюджет, общежитие Вам гарантировано. Для тех, кто будет учиться на платной основе, существует конкурс (поступающим по временному студенческому общежитие гарантировано).\nВ МИФИ девять общежитий: четыре квартирного типа, остальные - коридорного. \nПодробнее про общежития ▶️ <a href=\"https://admission.mephi.ru/about/dorm\">тык</a>"))
texts.append(BaseText(callback_text="text_exams",
                      text="\uD83D\uDE33 Есть ли возможность сдать внутренние вступительные экзамены вместо ЕГЭ?\n\nПоступать по вступительным испытаниям имеют право:\n\n✔ Иностранцы\n✔ Люди с инвалидностью\n✔ Россияне, окончившие школу за рубежом не позднее года до подачи документов и не сдававшие ЕГЭ\n✔ Абитуриенты, имеющие среднее профессиональное образование (выпускники колледжей, техникумов)\n✔ Абитуриенты, имеющие высшее образование (которые поступают на второе высшее).\n\nОстальных принимаем только по результатам ЕГЭ"))
texts.append(BaseText(callback_text="text_other",
                      text="👻 Другие вопросы есть на сайте приемной комиссии ▶️ <a href='https://clck.ru/3BqN6G'>тык</a>"))
texts.append(BaseText(callback_text="text_faculty",
                      text="\uD83E\uDD14 В чём уникальность нашего факультета?\n\nСтуденты ФБИУКСа в дальнейшем будут работать в <b>IT-сфере</b>: системные аналитики, бизнес-аналитики, проектировщики, разработчики, архитекторы информационных систем. \nНас интересуют IT-задачи, IT-стратегии, работа с большими данными. \n\n\uD83D\uDDA5️ В общем, мы ориентированы на <b>инновационную и предпринимательскую деятельность</b>: высокотехнологические startup-компании, IT-компании, цифровая экономика, страховое дело, банковское дело."))
texts.append(BaseText(callback_text="text_news_unsubscribed", text="❤️ Вы успешно подписались на рассылку!"))
texts.append(BaseText(callback_text="text_news_subscribed", text="💔 Вы отписались от рассылки"))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
# texts.append(BaseText(callback_text="", text=""))
for text in texts:
    print(text.callback_text)
    text.text = text.text.encode('raw_unicode_escape').decode('unicode_escape').encode('utf-16_BE',
                                                                                       'surrogatepass').decode(
        'utf-16_BE')
    create_text(db=next(get_db()), text=text)
