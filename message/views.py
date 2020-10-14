from django.shortcuts import render, HttpResponse
from africastalking.utils import send_sms_via_at
from .forms import FileUploadForm

# Create your views here.


def bulk_sms_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        return render(request, "message/file_upload.html", {"form": form})
