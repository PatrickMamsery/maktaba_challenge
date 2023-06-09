from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
# from django.db.models import Q
from .models import CSVFile
from .forms import CSVFileUploadForm
import csv
import os
from maktaba_challenge.settings import BASE_DIR

def home(request):
    if request.user.is_authenticated is not True:
        return redirect("/login")
    
    return render(request, "home.html")


def landing(request):
    return render(request, "landing.html")


def error(request):
    return render(request, "error.html")


def uploaded_docs(request):
    if request.user.is_authenticated is not True:
        return redirect("/login")
    
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
        # paginator = Paginator(files, 10)
        # page = request.GET.get('page')
        # files = paginator.get_page(page)
        uploads = CSVFile.objects.all().order_by('-uploaded_at')
        context = {'form': form, 'uploads': uploads}
    return render(request, "upload.html", context)


def file_details(request, id):
    if request.user.is_authenticated is not True:
        return redirect("/login")
    
    file = CSVFile.objects.get(id=id)
    data = csv.reader(file.file.read().decode('utf-8').splitlines())
    headers = next(data) # assumption that first row is header information
    rows = [row for row in data]

    # implement pagination
    paginator = Paginator(rows, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    if data is not None:
        context = {
            'file': file, 
            'headers': headers, 
            'rows': page_obj, 
            'loaded': True,
            'is_paginated': True if paginator.num_pages > 1 else False,
            'page': page_obj
        }
        return render(request, 'file_detail.html', context)
    else:
        return render(request, "file_detail.html", {'msg': 'Nothing Found'})


def export_csv(request, id):
    if request.user.is_authenticated is not True:
        return redirect("/login")
    
    # file = CSVFile.objects.get(id=id)
    file_path = os.path.join(BASE_DIR, "media/"+CSVFile.objects.get(id=id).filename())
    file = open(file_path, "r", "utf-8", error="ignore")
    data = csv.reader(file.file.read().decode('utf-8').splitlines())
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file}.csv"'
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

