from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from django.core.files.storage import default_storage, Storage
import os
import sqlite3
from django.core.files.uploadedfile import InMemoryUploadedFile

def hello(request):
    return HttpResponse("Hello world ! ")

def runoob(request):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT * FROM TASK')
    contents = c.fetchall()
    conn.close()
    return render(request, "runoob.html", {"tasks" : contents})


class Task:
    def __init__(self, model_file_name, status, result_file_name):
        self.model_file_name = model_file_name
        self.status = status
        self.result_file_name = result_file_name

def save_file(model_file):
    # 计算文件大小
    file_size_bytes = model_file.size
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024

    # 创建文件大小信息字符串
    file_size_info = f'文件大小：{file_size_mb:.2f} MB'

    # 将文件大小信息写入到文件中
    # name, ext = os.path.splitext(model_file.name)
    # result_file = "upload/" + name + "_result_" + ext
    save_path = "upload/" + model_file.name
    filename = os.path.join(save_path)

    with open(filename, 'w') as f:
        f.write(file_size_info)

def create_task(request):
    if request.method == 'POST':
        model_file = request.FILES['modelFile']
        save_file(model_file)

    return HttpResponse('task completed')
