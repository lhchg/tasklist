from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from django.core.files.storage import default_storage, Storage
import os
import sqlite3
from django.core.files.uploadedfile import InMemoryUploadedFile
from . import settings


def hello(request):
    return HttpResponse("Hello world ! ")


def runoob(request):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT * FROM TASK')
    contents = c.fetchall()
    conn.close()
    return render(request, "runoob.html", {"tasks" : contents})

def insert_database(model_file, platform):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO TASK (MODULE_FILE_NAME,PALTFORM, STATUS)\
    VALUES (?, ?, ?)", (model_file.name, platform, "progress..."))
    conn.commit()
    conn.close()

def save_file(model_file, platform):
    save_path = os.path.join(settings.MEDIA_ROOT, model_file.name)
    with open(save_path, 'wb') as destination:
        for chunk in model_file.chunks():
            destination.write(chunk)

    insert_database(model_file, platform)

def progress(model_file, platform):
    file_size_bytes = model_file.size
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024

    file_size_info = f'file size is：{file_size_mb:.2f} MB'

    name, ext = os.path.splitext(model_file.name)
    result_file = "result/" + name + "_result" + ".txt"
    filename = os.path.join(result_file)

    with open(filename, 'w') as f:
        f.write(file_size_info + "\n")
        f.write(platform)


def create_task(request):
    if request.method == 'POST':
        model_file = request.FILES['modelFile']
        platform = request.POST.get('platform')

        save_file(model_file, platform)
        progress(model_file, platform)

    return HttpResponse('task completed')
