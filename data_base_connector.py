import sqlite3
import datetime

db = sqlite3.connect("database.db")
cursor = db.cursor()


def get_model_id(model):
    cursor.execute("SELECT id FROM models WHERE ModelLogin = ?", [model])
    return cursor.fetchone()[0]


def get_account_id(account):
    cursor.execute("SELECT id FROM accounts WHERE Login = ? AND Password = ?", account[:2])
    return cursor.fetchone()[0]


def get_models():
    return [value[0] for value in cursor.execute("SELECT ModelLogin FROM models")]


def get_model(id):
    cursor.execute("SELECT ModelLogin FROM models WHERE Id = ?", [id])
    return cursor.fetchone()[0]


def get_accounts():
    return [value[1:] for value in cursor.execute("SELECT * FROM accounts")]


def get_subs(account, last=False):
    account_id = get_account_id(account)
    if last:
        cursor.execute("SELECT ModelId, Date FROM subs WHERE AccountId = ? ORDER BY Date DESC", [account_id])
        return cursor.fetchone()

    models_id = [value[0] for value in
                 cursor.execute("SELECT ModelId FROM subs WHERE AccountId = ?", [account_id])]
    return models_id


def add_models(models):
    temp = len(get_models())
    for model in models:
        cursor.execute(f"INSERT INTO models(ModelLogin) VALUES(?)", [model])
        db.commit()
    print("Кол-во новых записей : ", len(get_models()) - temp)


def add_accounts(accounts):
    for account in accounts:
        cursor.execute("INSERT INTO accounts(Login, Password) VALUES(?, ?)", account)
        db.commit()


def add_sub(model, account, date):
    cursor.execute(
        "INSERT INTO subs(ModelId, AccountId, Date) VALUES(?, ?, ?)",
        [get_model_id(model), get_account_id(account), date]
    )
    db.commit()


def delete_model(model):
    pass


def get_today_subs(account):
    account_id = get_account_id(account)
    cursor.execute("SELECT Date FROM subs WHERE AccountId = ? ORDER BY Date DESC", [account_id])
    today = datetime.datetime.today().date()
    last_100_subs = [datetime.datetime.strptime(value[0][:10], '%Y-%m-%d').date() for value in cursor.fetchmany(100)]
    return len(list(filter(lambda x: x == today, last_100_subs)))
