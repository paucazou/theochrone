#!/usr/bin/python3
# -*-coding:Utf-8 -*
from django.conf.urls import url
from . import views

urlpatterns = [
        url(r"^accueil$",views.home,name="accueil"),
        url(r"^date_seule$",views.date_transfert),
        url(r"^mot_clef$",views.mc_transfert),
        url(r"^mois$",views.mois_transfert),
        url(r"^contact$", views.contact),
        url(r"^widget$",views.widget),
        url(r"^download$",views.download),
        url(r"^export$",views.export),
        ]

