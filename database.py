import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()


def initialize():
    cur.execute(f'CREATE TABLE IF NOT EXISTS servers(serverId primary key, moderId)')


def add_server(server_id):
    try:
        server = (server_id, None)
        cur.execute('INSERT INTO servers(serverId, moderId) VALUES (?, ?)', server)
        conn.commit()
    except sqlite3.Error as error:
        print("Ошибка: ", error)


def set_moder(server_id, moder_id):
    try:
        print("Success")
        data = (moder_id, server_id)
        query = """UPDATE servers SET moderId = ? WHERE serverId = ?"""
        cur.execute(query, data)
        conn.commit()
    except sqlite3.Error as error:
        print("Ошибка: ", error)


def check(server):
    cur.execute("SELECT moderID FROM servers WHERE serverId = ?", (server,))
    return cur.fetchone()[0]


def test():
    cur.execute("SELECT serverID FROM servers")
    massive = cur.fetchall()
    guild = []
    for i in range(len(massive)):
        guild.append(massive[i][0])
    return guild
