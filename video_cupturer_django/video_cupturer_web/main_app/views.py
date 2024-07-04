from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .cv_capturer import vidio_cupture
from .models import UserFileUpload, UserFileDetected
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.db import connection

def index(request):
    return render(request, "index.html")

@login_required
def file_upload(request):
     if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Здесь можно добавить валидацию файла
        
        # Обработка файла (например, сохранение на диск)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        file_url = fs.url(filename)
        # fs.location(filename)
        # file_url = vidio_cupture(filename, file_url)
        # file_url = "/media/output/" + file_url 
        file_upload = UserFileUpload.objects.create(
            filename = filename,
            fileurl = file_url,
            master = request.user
        )
        # После обработки файла можно вернуть ответ с информацией о файле
        return render(request, 'file_upload.html', {
            'file_url': file_url
        })
    
     return render(request, 'file_upload.html')
@login_required
def user_files(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from main_app_userfileupload left join (select fileurl_master_file , (fileurl) as `fileurl_detected` from  main_app_userfiledetected) as `q1`  on  main_app_userfileupload.fileurl = q1.fileurl_master_file  where id is not null and master_id =%s ",[request.user.id])
        files = cursor.fetchall()   # получаем все строки

        return render(request, 'user_files.html', {
            'files': files
        })
@login_required
def file_handle(request):
    if request.method == 'POST':
        file_url = request.POST.get("file_url")
        filename = request.POST.get("filename")
        fileurl_master = file_url
        filename = vidio_cupture(filename, file_url)
        file_url = "/media/output/" + filename

        file_detected = UserFileDetected.objects.create(
                filename = filename,
                fileurl = file_url,
                master = request.user,
                fileurl_master_file = fileurl_master
            )
        file_detected = {"file_detected": True} 
        return JsonResponse(file_detected,safe=False)
    return redirect("user_files/")
        
    
    
