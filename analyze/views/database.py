import sqlite3

def insert_database(model_file, platform):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO TASK (MODULE_FILE_NAME,PALTFORM, STATUS)\
    VALUES (?, ?, ?)", (model_file, platform, "progress..."))
    inserted_id = c.lastrowid
    conn.commit()
    conn.close()
    return inserted_id

def update_database(id, result_file, model_file):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("UPDATE TASK set STATUS = 'done', RESULT_FILE = ? where ID= ?", (result_file, id))
    conn.commit()
    conn.close()

def select_database():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT * FROM TASK ORDER BY timestamp DESC')
    contents = c.fetchall()
    conn.close()
    return contents
