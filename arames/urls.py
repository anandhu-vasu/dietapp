"""arames URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.urls import include
from django.conf.urls import handler404
from dietapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('',include('django.contrib.auth.urls')),
    path('signup/',views.signup,name='signup'),
    path('form/', views.form, name='form'),
    path('diet/', views.diet, name='diet'),
    path('mom/', views.mom, name='mom'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/<slug:nav>/',views.dashboard,name='dashboard'),
]
handler404 = 'dietapp.views.error404'