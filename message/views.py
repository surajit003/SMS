from django.shortcuts import render
from .forms import FileUploadForm
from message.file_parser import validate_file_upload
# Create your views here.


def file_upload(request):
    if request.method == "GET":
        form = FileUploadForm()
        return render(request, "message/file_upload.html", {"form": form})
    if request.method == "POST":
        form = FileUploadForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save()
            validate_file_upload(instance.id)

        return render(request, "message/file_upload.html", {"form": form})
