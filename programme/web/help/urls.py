#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
from django.conf.urls import url
from . import views

urlpatterns = [
        url(r"^main$",views.main),
        ]
