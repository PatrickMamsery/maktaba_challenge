from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'uploads', CSVFileViewSet, basename='uploads')

urlpatterns = [
    path('', include(router.urls), name='upload_api'),
    # path('file/<int:file_id>/', file_data_api, name='file_data_api')
]