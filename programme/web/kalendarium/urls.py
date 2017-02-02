#!/usr/bin/python3
# -*-coding:Utf-8 -*
from django.conf.urls import url
from . import views

urlpatterns = [
        url(r"^accueil$",views.home),
        ]

