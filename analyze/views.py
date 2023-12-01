
import sqlite3
from datetime import datetime, timedelta
import pytz
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from django.core.files.storage import default_storage, Storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse
from rpyc.utils.server import ThreadedServer
from . import settings
import time
import os
import sqlite3
import _thread
import rpyc
import threading

class FileUploadService(rpyc.Service):
    uploaded_filename = None
    server = None
    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def exposed_upload_file(self, filepath, content):
        #time.sleep(10)
        replaced_string = filepath.replace('\\', '/')
        filename = replaced_string.split('/')[-1]
        savefile = "upload/" + filename
        with open(savefile, 'wb') as file:
            file.write(content)

        if FileUploadService.server:
            FileUploadService.uploaded_filename = filename
            time.sleep(2)
            FileUploadService.server.close()

def get_uploaded_filename(request):
    uploaded_filename = None
    while uploaded_filename is None:
        uploaded_filename = FileUploadService.uploaded_filename
        FileUploadService.uploaded_filename = None
    return HttpResponse(uploaded_filename)

def upload_listen():
    server = ThreadedServer(FileUploadService, port=12345)
    FileUploadService.server = server
    server.start()

def start_upload_service(request):
    # 启动文件上传服务
    threading.Thread(target=upload_listen).start()
    return HttpResponse('文件上传服务已完成！')


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

def save_file(model_file, platform):
    id = insert_database(model_file, platform)
    return id

def progress(id, model_file, platform):
    #time.sleep(20)
    cal_file = "upload/" + model_file
    size = os.path.getsize(cal_file)
    file_size_bytes = size
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024

    file_size_info = f'file size is：{file_size_mb:.2f} MB'

    name, ext = os.path.splitext(model_file)
    result_path = "result/"
    result_file = name + "_result" + ".txt"
    filename = os.path.join(result_path + result_file)

    with open(filename, 'w') as f:
        f.write(file_size_info + "\n")
        f.write(platform)
    update_database(id, result_file, model_file)


def runoob(request):

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT * FROM TASK')
    contents = c.fetchall()
    conn.close()

    tasks = []
    for content in contents:
        timestamp = content[1]
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        upload_file = "upload/" + content[2]
        model_file_exists = os.path.exists(upload_file)
        content = content + (model_file_exists,)
        if content[4] is not None:
            result_file = "result/" + content[5]
            result_file_exists = os.path.exists(result_file)

        else:
            result_file_exists = False
        content = content + (result_file_exists, timestamp_str)
        tasks.append(content)


    return render(request, "runoob.html", {"tasks" : tasks})



def create_task(request):
    if request.method == 'POST':
        model_file = request.POST.get('modelFile')
        platform = request.POST.get('platform')

        id = save_file(model_file, platform)
        try:
            _thread.start_new_thread(progress, (id, model_file, platform))
        except:
            return HttpResponse('something error')

    return HttpResponse('task completed')
