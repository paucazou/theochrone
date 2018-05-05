#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module is intented to export
Theochrone results into other formats, such as csv,
in order to be used in other softwares"""
import annus
import arrow
import csv
import datetime
import ics
import officia
import textwrap


def _data_wrapper(feast, lang: str, rank: int) -> tuple:
    """Extract data from feast, which is a Fete or Fete like object.
    rank is the rank of the feast in the day
    Return a tuple : name, description, start, end"""
    descriptions = {'fr':textwrap.dedent("""\
                    État : {}
                    Classe : {}
                    Catégorie : {}
                    Temps liturgique : {}
                    Couleur : {}
                    Station : {}""")}
    state = {"fr":['célébrée','peut être célébrée','peut être célébrée ou commémorée','commémorée','omise']}
    category = {"fr":['Temporal','Sanctoral']}
    classe = {"fr":[0,1,2,3,4,"Commémoraison","messe Pro Aliquibus Locis"]}
    no_info = '/'
    ## state of feast
    if feast.omission:
        fstate = state[lang][-1]
    elif feast.celebree:
        fstate = state[lang][0]
    elif feast.commemoraison and feast.peut_etre_celebree:
        fstate = state[lang][2]
    elif feast.peut_etre_celebree:
        fstate = state[lang][1]
    else:
        fstate = state[lang][-2]
    ## station
    if feast.__dict__.get('station',{lang:None})[lang]:
        fstation = feast.station[lang]
    else:
        fstation = no_info
    ## category
    if not feast.sanctoral and not feast.temporal:
        fcategory = no_info
    else:
        fcategory = category[lang][feast.sanctoral]
    # setting description
    description = descriptions[lang].format(
                    fstate,
                    classe[lang][feast.degre],
                    fcategory,
                    officia.affiche_temps_liturgique(feast,lang),
                    feast.couleur, # TODO not good for other languages
                    fstation)
    # dates
    fdate = arrow.Arrow(feast.date.year,feast.date.month,feast.date.day)
    fdate = fdate.shift(seconds = rank)
    
    return feast.nom[lang], description, fdate 

def main(start: datetime.date,stop: datetime.date, lang: str,
           stream, proper='roman', ordo=1962, file_ext='ics', **options) -> bool:
    """Turn data into a file from start to stop.
    stream is a stream where data will be written
    proper & ordo select data sent
    options are named arguments with a bool as value
    Valid options are : 'pal' (Pro Aliquibus Locis) # include martyrology ? TODO
    Return True"""
    # checking errors
    valid_options = {'pal'}
    if len(set(options).intersection(valid_options)) != len(options):
        raise KeyError("{}\nAn invalid option has been introduced. Please use one of the valid options: {}".format(*options.keys(),*valid_options))
    incorrect_values = [val for val in options.values() if not isinstance(val,bool)]
    if incorrect_values:
        raise ValueError("{}\nAn invalid value has been given in options. Please use only booleans.".format(incorrect_values[0]))

    types = { 'csv':_to_csv,
            'ics':_to_ics}
    if file_ext not in types:
        raise ValueError("{} is not a valid type. Please select a valid one: {}".format(file_ext,*types.keys()))
    # collecting data
    liturgycal = annus.LiturgicalCalendar(proper=proper,ordo=ordo)
    liturgycal(start.year,stop.year)
    # dispatching to custom function
    types[file_ext](start,stop,lang, liturgycal,stream, **options)
    return True

def _to_ics(start: datetime.date, stop: datetime.date, lang: str,
        liturgycal, stream, **options) -> bool:
    """Turn data into a ics file.
    liturgycal is a liturgical calendar with requested start and stop
    stream is a stream where ics calendar will be written
    Return True"""
    calendar = ics.Calendar()
    for day in liturgycal[start:stop]:
        for i, feast in enumerate(day):
            if not feast.pal or options.get('pal',False):
                event = ics.Event()
                raw_data = _data_wrapper(feast,lang,i)
                event.name = raw_data[0]
                event.description = raw_data[1]
                event.begin = raw_data[2]
                calendar.events.append(event)
    stream.writelines(calendar)
    return True



def _to_csv(start: datetime.date, stop: datetime.date, lang: str,
           liturgycal, stream, **options) -> bool:
    """Turn data into a csv file.
    liturgycal is a liturgical calendar with requested start and stop
    stream is a stream where csv will be written
    Return True"""
    # formatting csv writer
    fields = ['Subject','Description','Start Date','End Date']
    writer = csv.DictWriter(stream,fieldnames=fields,dialect='excel')
    writer.writeheader()
    # writing data
    for day in liturgycal[start:stop]:
        for i,feast in enumerate(day):
            if not feast.pal or options.get('pal',False):
                description = _data_wrapper(feast,lang,i)[1]
                data = {'Subject':feast.nom[lang],
                        'Description':description,
                        'Start Date': feast.date.strftime('%x'), # not safe, cause it depends on locale # WARNING 
                        'End Date':feast.date.strftime('%x')}
                writer.writerow(data)
    return True # return file as string ? as iostream ? TODO



