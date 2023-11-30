import time

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from django.core.files.storage import default_storage, Storage
import os
import sqlite3
from django.core.files.uploadedfile import InMemoryUploadedFile
from . import settings
import _thread
from django.contrib.staticfiles.storage import staticfiles_storage


def insert_database(model_file, platform):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO TASK (MODULE_FILE_NAME,PALTFORM, STATUS)\
    VALUES (?, ?, ?)", (model_file.name, platform, "progress..."))
    conn.commit()
    conn.close()

def update_database(result_file, model_file):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("UPDATE TASK set STATUS = 'done', RESULT_FILE = ? where MODULE_FILE_NAME= ?", (result_file, model_file.name))
    conn.commit()
    conn.close()

def save_file(model_file, platform):
    save_path = os.path.join(settings.MODEL_ROOT, model_file.name)
    with open(save_path, 'wb') as destination:
        for chunk in model_file.chunks():
            destination.write(chunk)

    insert_database(model_file, platform)

def progress(model_file, platform):
    #time.sleep(20)
    file_size_bytes = model_file.size
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024

    file_size_info = f'file size is：{file_size_mb:.2f} MB'

    name, ext = os.path.splitext(model_file.name)
    result_path = "result/"
    result_file = name + "_result" + ".txt"
    # result_file = "result/" + name + "_result" + ".txt"
    filename = os.path.join(result_path + result_file)

    with open(filename, 'w') as f:
        f.write(file_size_info + "\n")
        f.write(platform)
    update_database(result_file, model_file)


def runoob(request):

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT * FROM TASK')
    contents = c.fetchall()
    conn.close()

    tasks = []

    for content in contents:
        upload_file = "upload/" + content[1]
        model_file_exists = os.path.exists(upload_file)
        content = content + (model_file_exists,)
        if content[4] is not None:
            result_file = "result/" + content[4]
            result_file_exists = os.path.exists(result_file)

        else:
            result_file_exists = False
        content = content + (result_file_exists, )
        tasks.append(content)


    return render(request, "runoob.html", {"tasks" : tasks})



def create_task(request):
    if request.method == 'POST':
        model_file = request.FILES['modelFile']
        platform = request.POST.get('platform')

        save_file(model_file, platform)
        try:
            _thread.start_new_thread(progress, (model_file, platform))
        except:
            return HttpResponse("something wrong")

    return HttpResponse('task completed')
