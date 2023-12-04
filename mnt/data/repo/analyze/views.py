import datetime

from analyze.views import HttpResponse, progress, save_file
from django.core.files.storage import default_storage


def create_task(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('modelFileInput')
        platform = request.POST.get('platform')

        if uploaded_file is not None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            unique_file_name = f"{timestamp}_{uploaded_file.name}"
            model_file = default_storage.save(unique_file_name, uploaded_file)
        else:
            model_file = request.POST.get('modelFile')

        id = save_file(model_file, platform)
        try:
            _thread.start_new_thread(progress, (id, model_file, platform))
        except:
            return HttpResponse('something error')

    return HttpResponse('task completed')
