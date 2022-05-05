"""apiproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from . import views
#to start python manage.py runserver 3000
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.arara),
    path('forgot_password/',views.forgot_password),
    path('invite_user_to_become_admin/',views.invite_user_to_become_admin),
    path('Send_user_his_win_info_in_rulate/',views.Send_user_his_win_info_in_rulate),
    #path('send_user_info_about_his_payment/',views.send_user_info_about_his_payment), not sure
]
