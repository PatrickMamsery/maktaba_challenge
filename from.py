from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

import os
import json
from freezer.settings import BASE_DIR, MEDIA_ROOT
from .forms import MasterDataFileForm
from .models import MasterDataFile


import datetime
import csv

def get_recent_uploaded():
    uploads = MasterDataFile.objects.filter(active = True).order_by('-id')
    if uploads:
        return uploads[0]
    else:
        return None


def home(request):
    return render(request, "home.html")

def search_code(code):
    target_file = get_recent_uploaded()
    if target_file is None:
        return False
    file_path = os.path.join(BASE_DIR, "media/"+target_file.filename())

    file = open(file_path, 'r', encoding='utf-8', errors='ignore')
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if row['COOLER TAG'] == str(code) or row['OUTLET TAG'] == str(code):
                    return row
            except:
                pass

    return None


# Create your views here.
def search_view(request):
    target_file = get_recent_uploaded()
    if target_file is not None:
        date_time = target_file.file_date.strftime("%d/%m/%Y, %H:%M:%S")
    else:
        date_time = "No File Available !"

    if request.POST:
        code_post = request.POST['cooler_no']
        data = search_code(code_post)
        if data is False:
            return redirect("/error")

        if data is not None:
            context = {
                'loaded': True,
                'map': False,
                "data_last_update": date_time,
                'outlet_no': data['OUTLET NO'],
                'outlet_name': data['CURRENT OUTLET NAME'],
                'outlet_location': data['CURRENT LOCATION'],
                'mobile_number': data['CURRENT MOBILE\TEL NO'],
                'description_model': data['Description MODEL ID'],
                'cooler_tag': data['COOLER TAG'],
                'region': data['REGION'],
                'rad_name': data['RAD NAME'],
                'asm_name': data['ASM NAME'],
                'occd_training_name': data['OCCD TRADING NAME'],
                'last_scanned': data['LAST SCANNED'],
                'route_name': data['ROUTE NAME'],
                'current_location': data['CURRENT LOCATION'],
                'fi_system_status': data['FI System status']
            }
            return render(request, "index.html", context)
        else:
            return render(request, "index.html", {'msg': 'nothing Found',"data_last_update": date_time})

    return render(request, "index.html", {"data_last_update": date_time})


def cooler_verification(request, time_jump, center):
    # *
    time_jump = time_jump
    center = center
    # *
    date_jump = datetime.datetime.today() - datetime.timedelta(weeks=time_jump)
    row_list = []

    target_file = get_recent_uploaded()
    if target_file is None:
        return redirect("/error")

    file_path = os.path.join(BASE_DIR, "media/"+target_file.filename())
    file = open(file_path, 'r', encoding='utf-8', errors='ignore')
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # date
                last_scanned = row['LAST SCANNED']
                scan_date = last_scanned
                distribution_center = row['OCCD TRADING NAME']
                rad_name = row['RAD NAME']

                if center != distribution_center:
                    continue
                try:
                    last_scanned = datetime.datetime.strptime(last_scanned, '%Y-%m-%d')
                except:
                    try:
                        last_scanned = datetime.datetime.strptime(last_scanned, '%d/%m/%Y')
                    except:
                        pass
                
                if type(last_scanned) != str and last_scanned < date_jump:

                    lat = row['Lat'] or row['lat']
                    lat = float(lat)
                    longs = row['Long'] or row['long']
                    longs = float(longs)

                    geometry = {
                        "latitude": lat,
                        "longitude": longs,
                        "rad": row['RAD NAME'],
                        "asm": row['ASM NAME'],
                        "last_scanned": scan_date,
                        "outlet_number": row['OUTLET NO'],
                        "outlet_name": row['CURRENT OUTLET NAME'],
                        "mobile_number": row['CURRENT MOBILE\TEL NO'],
                        "outlet_location": row['CURRENT LOCATION']
                    }

                    row_list.append(geometry)
                else:
                    # target ahead of date
                    pass
            except:
                pass

    data = json.dumps(row_list)
    context = {
        "row_list": data,
        "data_last_update": target_file.file_date
    }


    return render(request, "cooler_verification.html", context)

def rad_cooler_verification(request, time_jump, center):
    # *
    time_jump = time_jump
    center = center
    # *
    date_jump = datetime.datetime.today() - datetime.timedelta(weeks=time_jump)
    row_list = []

    target_file = get_recent_uploaded()
    if target_file is None:
        return redirect("/error")

    file_path = os.path.join(BASE_DIR, "media/"+target_file.filename())

    file = open(file_path, 'r', encoding='utf-8', errors='ignore')
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # date
                last_scanned = row['LAST SCANNED']
                scan_date = last_scanned
                distribution_center = row['OCCD TRADING NAME']
                rad_name = row['RAD NAME']

                if center != rad_name:
                    continue

                try:
                    last_scanned = datetime.datetime.strptime(last_scanned, '%Y-%m-%d')
                except:
                    try:
                        last_scanned = datetime.datetime.strptime(last_scanned, '%d/%m/%Y')
                    except:
                        pass
                
                if type(last_scanned) != str and last_scanned < date_jump:
                    
                    lat = row['Lat'] or row['lat']
                    longs = row['Long'] or row['long']

                    geometry = {
                        "latitude": lat,
                        "longitude": longs,
                        "rad": row['RAD NAME'],
                        "asm": row['ASM NAME'],
                        "last_scanned": scan_date,
                        "outlet_number": row['OUTLET NO'],
                        "outlet_name": row['CURRENT OUTLET NAME'],
                        "mobile_number": row['CURRENT MOBILE\TEL NO'],
                        "outlet_location": row['CURRENT LOCATION']
                    }

                        
                    row_list.append(geometry)
                else:
                    # target ahead of date
                    pass
            except:
                pass

    data = json.dumps(row_list)
    context = {
        "row_list": data,
        "data_last_update": target_file.file_date.strftime("%d/%m/%Y, %H:%M:%S")
    }

    return render(request, "cooler_verification.html", context)


def cooler_verification_blank(request):
    target_file = get_recent_uploaded()
    date_time = target_file.file_date.strftime("%d/%m/%Y, %H:%M:%S")
    context = {
        "data_last_update": date_time
    }
    return render(request, "cooler_verification.html", context)

def error(request):
    
    return render(request, "error.html")


def upload_file(request):
    if request.user.is_authenticated is not True:
        return redirect("/login")

    if request.method == 'POST':
        form = MasterDataFileForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/upload")
    else:
        uploads = MasterDataFile.objects.all().order_by('-id')
        form = MasterDataFileForm()
    return render(request, "upload.html", {'form': form, 'uploads': uploads})


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


def activate_file_view(request, file_id):
    if request.user.is_authenticated is not True:
        return redirect("/login")
    # deactivate other files
    MasterDataFile.objects.all().update(active=False)
    # activate file
    file = MasterDataFile.objects.get(id=file_id)
    file.active = True
    file.save()
    return redirect("/upload")


def check_missing_gaps(old_fields, new_fields):
    response = []
    for i in range(0, len(old_fields)):
        if old_fields[i] in new_fields:
            continue
        else:
            response.append(old_fields[i])

    return response

def is_valid_datetime(last_scanned):
    date_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d",
                    "%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M", "%m/%d/%Y",
                    "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y",
                    "%m-%d-%Y %H:%M:%S", "%m-%d-%Y %H:%M", "%m-%d-%Y",
                    "%d-%m-%Y %H:%M:%S", "%d-%m-%Y %H:%M", "%d-%m-%Y",
                    "%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M", "%Y.%m.%d",
                    "%d.%m.%Y %H:%M:%S", "%d.%m.%Y %H:%M", "%d.%m.%Y",
                    "%m.%d.%Y %H:%M:%S", "%m.%d.%Y %H:%M", "%m.%d.%Y",
                    "%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M", "%Y/%m/%d",
                    "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y"]
    for date_format in date_formats:
        try:
            datetime.datetime.strptime(last_scanned, date_format)
            return True
        except ValueError:
            pass
    return False

def get_percentage_change(base, new):
    if base == 0:
        return float('inf') if new > 0 else float('-inf')
    return int(100 - ((base - new) / base) * 100)


def verify_file_view(request, file_id):
    recent_active = MasterDataFile.objects.filter(active = True).order_by('-id')
    recent_uploaded = MasterDataFile.objects.get(id=file_id)

    file1 = open(os.path.join(BASE_DIR, "media/"+recent_active[0].filename()), 'r', encoding='utf-8', errors='ignore')
    file2 = open(os.path.join(BASE_DIR, "media/"+recent_uploaded.filename()), 'r', encoding='utf-8', errors='ignore')

    
    with file1 as csvfile, file2 as csvfile2:
        reader = csv.DictReader(csvfile)
        reader_new = csv.DictReader(csvfile2)
        old_field_names = reader.fieldnames
        new_field_names = reader_new.fieldnames
        # check fields
        missing_fields = []
        old_field_count = len(old_field_names)
        new_field_count = len(new_field_names)
        is_valid_length = (old_field_count == new_field_count)
        file_status = "Fields in new file match with the previous file"

        if is_valid_length is False:
            # print missing fields
            base = new_field_count;
            target = old_field_count

            if base < target:
                file_status = "Additional fields detected"
                missing_fields = check_missing_gaps(new_field_names, old_field_names)

            else:
                file_status = "Missing fields from previous file"
                missing_fields = check_missing_gaps(old_field_names, new_field_names)

        # check length
        count_old = 0
        count_new = 0
        last_scan_count = 0
        latitude_count = 0
        longitude_count = 0

        for row in reader:
            count_old += 1

        for row in reader_new:
            count_new += 1
            if row.get('Lat') or row.get('lat') or row.get('Latitude'):    
                data = row.get('Lat') or row.get('lat') or row.get('Latitude')
                try:
                    data = float(data)
                    if data != 0:
                        latitude_count += 1
                except:
                    pass

            if row.get('Long') or row.get('long') or row.get('Longitude'):
                data = row.get('Long') or row.get('long') or row.get('Longitude')
                try:
                    data = float(data)
                    if data != 0:
                        longitude_count += 1
                except:
                    pass

            if row['LAST SCANNED']:
                last_scanned = row['LAST SCANNED']
                if is_valid_datetime(last_scanned):
                    last_scan_count += 1


    context = {
        "uploaded_by": recent_uploaded.get_author(),
        "file_id": recent_uploaded.id,
        "file_name": file2.name,
        "file_format": file2.name.split(".")[-1],
        "missing_fields": missing_fields,
        "is_valid_length": is_valid_length,
        "old_field_count": old_field_count,
        "new_field_count": new_field_count,
        "field_difference": abs(old_field_count - new_field_count),
        "file_status": file_status,
        "count_old": count_old,
        "count_new": count_new,
        "record_difference": abs(count_old - count_new),
        "latitude_count": latitude_count,
        "longitude_count": longitude_count,
        "last_scan_count": last_scan_count,
        "latitude_percentage": get_percentage_change(count_new, latitude_count),
        "longitude_percentage": get_percentage_change(count_new, longitude_count),
        "last_scan_percentage": get_percentage_change(count_new, last_scan_count)
    }

    return render(request, "verify_file.html", context)


def delete_master_data_file(request, id):
    masterFile = MasterDataFile.objects.get(id=id)
    file_path = os.path.join(BASE_DIR , "media/"+masterFile.filename())
    os.remove(file_path)
    masterFile.delete()

    return redirect("/upload")