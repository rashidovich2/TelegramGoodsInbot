import sqlite3


from tgbot.data.config import PATH_DATABASE

# проверка записи локации
def is_lang(user_id):
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    query = '''select user_lang from storage_users where user_id = ?'''
    result = cur.execute(query, (user_id,)).fetchone()
    return result[0] is not None