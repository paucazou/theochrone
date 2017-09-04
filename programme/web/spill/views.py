from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

import datetime
import os
import sys
from .forms import Dispatch, Info
from kalendarium.forms import RechercheSimple

chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/../..')
sys.path.append(programme)
import annus
import officia

lyear = annus.LiturgicalCalendar()
language = 'fr'
host = 'theochrone.fr'
# Create your views here.

@xframe_options_exempt
def main(request):
    """The only view used by the whole app.
    Every other function inframe must redirect to this one"""
    dispatch = Dispatch(request.GET or None)
    page = 'day'
    if dispatch.is_valid():
        page = dispatch.cleaned_data['page']
    return render(request, 'spill/main.html',locals())

def day(request):
    """Returns value for one date"""
    # faire un forms pour la validation
    sentvalue = RechercheSimple(request.GET or None)
    if sentvalue.is_valid():
        day = sentvalue.cleaned_data['date_seule']
    else:
        day = datetime.date.today()
    lyear(day.year)
    data = lyear[day] # data of requested day
    hashtag = "resultup"
    link_to_day = datetime_to_link(day,host,hashtag)
    link_to_tomorrow = datetime_to_param(day + datetime.timedelta(1))
    link_to_yesterday = datetime_to_param(day - datetime.timedelta(1))
    return render(request,'spill/day.html',locals())
    
def create_module(request):
    """A function to help customers
    to create modules for their blogs"""
    pass

def test(request):
    """A view to test functions online"""
    return HttpResponse(str(request.META))

def datetime_to_link(day,host,hashtag='',s='s'): # should be moved to officia
    """Take a datetime.date like object
    and return a link to requested host.
    Hashtag can be set to point to a specific id on the page
    s is a s of https: default is 's'"""
    link = "http{}://{}/kalendarium/date_seule?date_seule_day={}&date_seule_month={}&date_seule_year={}#{}".format(
        s,host,day.day,day.month,day.year,hashtag)
    return link

def datetime_to_param(day):
    """Take a datetime.date like object
    return a link to requested host"""
    link = "day?date_seule_day={}&date_seule_month={}&date_seule_year={}".format(
        day.day,day.month,day.year)
    return link

def saveUrls(request):
    """This view save urls sent if in iframe"""
    info = Info(request.GET or None)
    file_path = os.path.expanduser('~/.urlsinfo.log')
    answer='Error'
    if info.is_valid():
        urlinfo = info.cleaned_data['urlinfo'].split('/')[2] + '\n'
        with open(file_path,'r') as file:
            lines = file.readlines()
        if urlinfo not in lines:
            with open(file_path,'a') as file:
                file.write(urlinfo+'\n')
        answer = 'Done'
    return HttpResponse(answer)

def day_to_static(start,stop,path):
    """This function return static pages corresponding to "day" views.
    start and stop are years.
    path is a directory with / at the end
    This function should be used in a django shell : web/manage.py shell"""
    import django.http
    def pseudo_day(request,data,day):
        """Imitates day behaviour in a static context"""
        hashtag = "resultup"
        link_to_day = datetime_to_link(day,host,hashtag)
        link_to_tomorrow = datetime_to_shtml(day + datetime.timedelta(1))
        link_to_yesterday = datetime_to_shtml(day - datetime.timedelta(1))
        months = ('','janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre')
        day = "{} {} {}".format(day.day,months[day.month],day.year)
        return render(request,'spill/day.html',locals())
    
    def datetime_to_shtml(day):
        """day is a datetime like object.
        This function returns a string as following :
        'dayYYYY-MM-DD.shtml'
        MM ans DD can be M and D if they are less than 10"""
        return """day{}-{}-{}.shtml""".format(day.year,day.month,day.day)
    
    lyear(start,stop)
    req = django.http.request.HttpRequest()
    req.META
    for data in lyear:
       day = data[0].date
       answer = pseudo_day(req,data,day)
       file_path = path + datetime_to_shtml(day)
       with open(file_path,'w') as file:
           file.write(answer.content.decode())
           
       
    
    
            
            
