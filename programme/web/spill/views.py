from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import get_language_from_request
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
    sentvalue = RechercheSimple(request.GET or None)
    if sentvalue.is_valid():
        day = sentvalue.cleaned_data['date_seule']
        pal = sentvalue.cleaned_data['pal']
    else:
        day = datetime.date.today()
        pal = False
    lang = get_language_from_request(request)
    lyear(day.year)
    data = lyear[day] # data of requested day
    hashtag = "resultup"
    link_to_day = officia.datetime_to_link(day,host,hashtag=hashtag)
    link_to_tomorrow = datetime_to_param(day + datetime.timedelta(1),pal=pal)
    link_to_yesterday = datetime_to_param(day - datetime.timedelta(1),pal=pal)
    return render(request,'spill/day.html',locals())

def day_mobile(request):
    """Similar to 'day' func.
    Should be use for mobile sites.
    Returns only the first feast found, except if the feast is a feria."""
    sentvalue = RechercheSimple(request.GET or None)
    if sentvalue.is_valid():
        day = sentvalue.cleaned_data['date_seule']
    else:
        day = datetime.date.today()
    lyear(day.year)
    data = lyear[day]
    index = len(data) > 1 and type(data[0]).__name__ == 'FeteFerie'
    feast = data[index]
    hashtag = "resultup"
    link_to_day = officia.datetime_to_link(day,host,hashtag=hashtag)
    return render(request,'spill/day_mobile.html',locals())    
    
def create_module(request):
    """A function to help customers
    to create modules for their blogs"""
    pass

def test(request):
    """A view to test functions online"""
    return HttpResponse(str(request.META))

def datetime_to_param(day,proper='roman',pal=False):
    """Take a datetime.date like object
    return a link to requested host"""
    link = "day?date_seule_day={}&date_seule_month={}&date_seule_year={}&pal={}".format(
            day.day,day.month,day.year,pal)
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

def day_to_static(start,stop,path,mobile=False): # TODO gérer les PAL en js directement dans les gabarits -> imposé pour la version mobile
    """This function return static pages corresponding to "day" views.
    start and stop are years.
    path is a directory with / at the end
    This function should be used in a django shell : web/manage.py shell"""
    import django.http
    def pseudo_day(request,data,day,mobile):
        """Imitates day behaviour in a static context"""
        hashtag = "resultup"
        link_to_day = officia.datetime_to_link(day,host,hashtag=hashtag)
        if not mobile:
            link_to_tomorrow = datetime_to_shtml(day + datetime.timedelta(1))
            link_to_yesterday = datetime_to_shtml(day - datetime.timedelta(1))
        months = ('','janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre')
        day = "{} {} {}".format(day.day,months[day.month],day.year)
        # add special classes for static files
        static_file = True
        pal = True
        # for mobile version
        if mobile:
            index = len(data) > 1 and type(data[0]).__name__ == 'FeteFerie'
            feast = data[index]
        # return
        return render(request,('spill/day.html','spill/day_mobile.html')[mobile],locals())
    
    def datetime_to_shtml(day,mobile=False):
        """day is a datetime like object.
        This function returns a string as following :
        'dayYYYY-MM-DD.shtml'
        MM ans DD can be M and D if they are less than 10"""
        return """{}day{}-{}-{}.shtml""".format(('','mob')[mobile],
            day.year,day.month,day.day)
    
    lyear(start,stop)
    req = django.http.request.HttpRequest()
    req.META
    for data in lyear:
       day = data[0].date
       answer = pseudo_day(req,data,day,mobile)
       file_path = path + datetime_to_shtml(day,mobile)
       with open(file_path,'w') as file:
           file.write(answer.content.decode())
           
       
    
    
            
            
