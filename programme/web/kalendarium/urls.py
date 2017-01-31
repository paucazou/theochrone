#!/usr/bin/python3
# -*-coding:Utf-8 -*
from . import views
from django.conf.urls import url
urlpatterns = [
        url(r"^accueil$",views.home),
        #url(r"^liste$",views.liste),
        ]
