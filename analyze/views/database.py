import sqlite3
import sys
import os

dlSystemDir = os.getenv('DL_SYSTEM_PATH')
if dlSystemDir is not None:
    db=os.path.join("%s/rpc_tasks/task.db" % dlSystemDir)
else:
    print("please set DL_SYSTEM_PATH")
    sys.exit()

def insert_database(model_file, platform):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO TASK (MODULE_FILE_NAME,PALTFORM, STATUS)\
    VALUES (?, ?, ?)", (model_file, platform, "progress..."))
    inserted_id = c.lastrowid
    conn.commit()
    conn.close()
    return inserted_id

def update_database(id, result_file, model_file):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("UPDATE TASK set STATUS = 'done', RESULT_FILE = ? where ID= ?", (result_file, id))
    conn.commit()
    conn.close()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def select_database():
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('SELECT * FROM TASK ORDER BY timestamp DESC')
    contents = c.fetchall()
    conn.close()
    return contents
