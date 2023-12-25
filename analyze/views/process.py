import time
import os

from analyze.views import database


def progress(id, model_file, platform):
    time.sleep(10)
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
    database.update_database(id, result_file, model_file)