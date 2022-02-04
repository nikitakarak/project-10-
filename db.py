import sqlite3
conn = sqlite3.connect('db11.db', check_same_thread=False)
cursor = conn.cursor()


def get_by_id (idd):

    cursor.execute('SELECT * FROM table_name WHERE column_0=?', [idd])
    if len(cursor.fetchall()) == 0:
        return 0
    else:
        return cursor.fetchall()
print(get_by_id(23))

def new_user(user_id: int,fio: str,classs:str):
	cursor.execute('INSERT INTO users (user_id, fio, class) VALUES (?, ?, ?)', (user_id,fio,classs))
	conn.commit()
new_user(12324,'Балль Михаил', '10И')