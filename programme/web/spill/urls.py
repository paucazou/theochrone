#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^main$",views.main),
    url(r'^day$',views.day),
    url(r'^day_mobile$',views.day_mobile),
    url(r'^test$',views.test),
    url(r'^saveurls$',views.saveUrls),
    ]
