# from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from upload.models import *
from .serializers import *
import csv

# Create your views here.
class CSVFileViewSet(viewsets.ModelViewSet):
    queryset = CSVFile.objects.all()
    serializer_class = CSVFileSerializer


# @api_view(['GET'])
# def file_data_api(request, file_id):
#     if request.method == 'GET':
#         try:
#             file = CSVFile.objects.get(id=file_id)
#         except:
#             return Response({'error': f'File with id={file_id} does not exist'}, status=404)

#         data = csv.reader(file.file.read().decode('utf-8').splitlines())
#         headers = next(data) # assumption that first row is header information
#         rows = [row for row in data]
        
#         #implement pagination
#         paginator = Paginator(rows, 10)
#         page_number = request.query_params.get('page')
#         page_obj = paginator.get_page(page_number)

#         structured_response = {
#             'headers': headers,
#             'rows': page_obj, 
#         }

#         return Response(structured_response, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)