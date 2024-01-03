from rpyc.utils.server import ThreadedServer
import rpyc
import threading
import time
from django.http import HttpResponse

# deprecate
class FileUploadService(rpyc.Service):
    uploaded_filename = None
    server = None
    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def exposed_upload_file(self, filepath, content):
        #time.sleep(10)
        print("exposed_upload_file")
        replaced_string = filepath.replace('\\', '/')
        filename = replaced_string.split('/')[-1]
        savefile = "upload/" + filename
        with open(savefile, 'wb') as file:
            print("saving file")
            file.write(content)
            print("file saved")

        if FileUploadService.server:
            FileUploadService.uploaded_filename = filename
            time.sleep(2)
            FileUploadService.server.close()

# deprecate
def get_uploaded_filename(request):
    print("get_uploaded_filename")
    uploaded_filename = None
    while uploaded_filename is None:
        #print(uploaded_filename)
        uploaded_filename = FileUploadService.uploaded_filename
        FileUploadService.uploaded_filename = None
    print(uploaded_filename)
    return HttpResponse(uploaded_filename)

# deprecate
def upload_listen():
    if FileUploadService.server:
        FileUploadService.server.close()
    server = ThreadedServer(FileUploadService, port=12345)
    FileUploadService.server = server
    server.start()

# deprecate
def start_upload_service(request):
    threading.Thread(target=upload_listen).start()
    return HttpResponse('start upload！')
