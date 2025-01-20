"""
URL configuration for hospital_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# hospital_website/urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from projectapp import views 

# from projectapp import download_files_as_zip


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('contact/', views.contact, name='contact'),
    path('index/', views.contact, name='index'),
    path('contactsubmit/', views.contact_view, name='contactsubmit'),
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    
    
    path('create_user/', views.create_user, name='create_user'),
    
    path("download/<int:year>/", views.download_files_as_zip, name="download_files_as_zip"),
    
    path('verify_user/', views.verify_user, name='verify_user'),
    path('user_history', views.user_history, name='user_history'),
     path('upload_data', views.upload_data, name='upload_data'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



