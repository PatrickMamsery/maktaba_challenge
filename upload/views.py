from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
# from django.core.paginator import Paginator
# from django.db.models import Q
from .models import CSVFile
from .forms import CSVFileUploadForm
import csv
# import os

def home(request):
    return render(request, "home.html")


def landing(request):
    return render(request, "landing.html")


def error(request):
    return render(request, "error.html")


def uploaded_docs(request):
    uploads = CSVFile.objects.all().order_by('-uploaded_at')
    context = {'uploads': uploads}
    return render(request, "docs.html", context)


# method to handle the upload of csv files
def upload(request):
    if request.user.is_authenticated is not True:
        return redirect("/login")

    if request.method == 'POST':
        form = CSVFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("upload")
    else:
        form = CSVFileUploadForm()
        # files = CSVFile.objects.all().order_by('-uploaded_at')
        # paginator = Paginator(files, 10)
        # page = request.GET.get('page')
        # files = paginator.get_page(page)
        uploads = CSVFile.objects.all().order_by('-id')
        context = {'form': form, 'files': uploads}
    return render(request, "upload.html", context)


def file_detail(request, id):
    file = CSVFile.objects.get(id=id)
    data = csv.reader(file.file.read().decode('utf-8').splitlines())
    context = {'file': file, 'data': data}
    return render(request, 'file_detail.html', context)


def export_csv(request, id):
    file = CSVFile.objects.get(id=id)
    data = csv.reader(file.file.read().decode('utf-8').splitlines())
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file.name}.csv"'
    writer = csv.writer(response)
    for row in data:
        writer.writerow(row)
    return response


def login_view(request):
    if request.POST:
        _user_name = request.POST['username']
        _password = request.POST['password']

        user = authenticate(username=_user_name, password=_password)

        if user is not None:
            login(request, user)
            return redirect("/upload")
        else:
            return redirect("/login")
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/login")

