from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse

import os
import sqlite3
import _thread

from analyze import settings
from analyze.views import process, backend, database
from django.core.paginator import Paginator

# deprecate
def tips(request):
    return render(request, "tips.html")


# deprecate
def save_file(model_file, platform):
    id = database.insert_database(model_file, platform)
    return id

# deprecate
def save_file_normal(model_file, platform):
    save_path = os.path.join(settings.MODEL_ROOT, model_file.name)
    with open(save_path, 'wb') as destination:
        for chunk in model_file.chunks():
            destination.write(chunk)

    id = database.insert_database(model_file.name, platform)
    return id

def runoob(request):
    client_ip = request.META.get('REMOTE_ADDR')
    print("REMOTE_ADDR:", client_ip)

    contents = database.select_database()

    tasks = []
    for content in contents:
        timestamp = content[1]
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        upload_file = "upload/" + content[2]
        model_file_exists = os.path.exists(upload_file)
        content = content + (model_file_exists,)
        if content[5] is not None:
            result_file = "result/" + content[5]
            result_file_exists = os.path.exists(result_file)

        else:
            result_file_exists = False
        content = content + (result_file_exists, timestamp_str)
        tasks.append(content)

    paginator = Paginator(tasks, 10)
    page_num = request.GET.get('page', 1)
    page_tasks = paginator.get_page(page_num)

    devices = backend.check_devices()
    backends = backend.check_backend()
    return render(request, "task.html", {"tasks": page_tasks, "devices": devices, "check_backend": backends})


# deprecate
def runoob_normal(request):

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('SELECT * FROM TASK ORDER BY timestamp DESC')
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
        if content[5] is not None:
            result_file = "result/" + content[5]
            result_file_exists = os.path.exists(result_file)

        else:
            result_file_exists = False
        content = content + (result_file_exists, timestamp_str)
        tasks.append(content)


    return render(request, "runoob_normal.html", {"tasks" : tasks})



# deprecate
def create_task(request):
    if request.method == 'POST':
        model_file = request.POST.get('modelFile')
        platform = request.POST.get('platform')

        id = save_file(model_file, platform)
        try:
            _thread.start_new_thread(process.progress, (id, model_file, platform))
        except:
            return HttpResponse('something error')

    return HttpResponse('task completed')

# deprecate
def create_task_normal(request):
    if request.method == 'POST':
        model_file = request.FILES['modelFile']
        platform = request.POST.get('platform')

        id = save_file_normal(model_file, platform)
        try:
            _thread.start_new_thread(process.progress, (id, model_file.name, platform))
        except:
            return HttpResponse('something error')

    return HttpResponse('task completed')
