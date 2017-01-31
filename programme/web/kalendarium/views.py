from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import os

# Create your views here.

def home(request):
    """A function which defines homepage"""
    os.chdir("/home/partage/.scripts/projet_liturgie/wip_fetes/programme")
    retour, err = subprocess.Popen('./theochrone.py', stdout=subprocess.PIPE, shell=True).communicate()
    return HttpResponse(retour)
