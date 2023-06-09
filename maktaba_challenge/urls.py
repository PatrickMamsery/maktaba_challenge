"""
URL configuration for maktaba_challenge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from upload.views import home, landing, error, file_details, login_view, logout_view, upload, export_csv, uploaded_docs

urlpatterns = [
    path('', landing, name='landing'),
    path('home', home, name='home'),
    path('login', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('error', error, name='error'),
    path('upload', upload, name='upload'),
    path('uploaded_docs', uploaded_docs, name='uploaded_docs'),
    path('details/<int:id>', file_details, name='file_details'),
    path('export/<int:id>', export_csv, name='export'),
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    #API
    path('api/v1/', include('api.urls'))
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
