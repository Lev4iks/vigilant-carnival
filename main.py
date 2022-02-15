# Импорт нужных библиотек и скриптов
from models_parser import parse_models, set_up_parser
import data_base_connector as db
import datetime
import time
import bot
import app


def main():
    # --------------------------- Работа с БД ---------------------------

    # Получаем аккаунты
    accounts = db.get_accounts()

    # Получаем модели
    models = db.get_models()

    # Получаем коментарии
    comments = db.get_comments()

    # --------------------------- Работа с БД ---------------------------

    # --------------------------- Работа с Ботом ---------------------------

    bot.models = models

    bot.accounts = accounts

    bot.comments = comments

    # --------------------------- Работа с Ботом ---------------------------

    # --------------------------- Работа с Парсером ---------------------------

    # if (datetime.datetime.today().date() - db.get_last_parse_date()).days >= 3:
    #     parse_models(set_up_parser())
    #     print("Прошло 3 дня, нужно спарсить новые модели")
    # else:
    #     print("Три дня не прошло, парсить нельзя")
    #     print("Дата последнего парсинга : ", db.get_last_parse_date())
    # time.sleep(5)

    # --------------------------- Работа с Парсером ---------------------------

    # --------------------------- Работа с Интерфейсом ---------------------------

    root = app.Tk()

    application = app.Application(parent=root)

    application.mainloop()

    # --------------------------- Работа с Интерфейсом ---------------------------


# Запускаем бота
if __name__ == '__main__':
    # try:
    main()
    # except Exception as err:
    #     with open('log_main.txt', 'w') as f:
    #         f.write(f"Ошибка - {err} {type(err)=}, {err.args}, {datetime.datetime.now()}")
    #         f.close()
