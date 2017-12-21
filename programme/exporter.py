#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module is intented to export
Theochrone results into other formats, such as csv,
in order to be used in other softwares"""
import annus
import csv
import officia
import textwrap

def to_csv(start: int,stop: int,file_path: str,lang: str,
           proper='romanus', ordo=1962, **options) -> bool:
    """Turn data into a csv file from year start to year stop.
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
    # formatting csv writer
    fields = ['Subject','Description','Start Date','End Date']
    csv_file = open(file_path,'w',newline='')
    writer = csv.DictWriter(csv_file,fieldnames=fields,dialect='excel')
    writer.writeheader()
    # collecting data
    liturgycal = annus.LiturgicalCalendar(proper=proper,ordo=ordo)
    liturgycal(start,stop)
    # writing data
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
    for day in liturgycal:
        for feast in day:
            if not feast.pal or options.get('pal',False):
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
                data = {'Subject':feast.nom[lang],
                        'Description':description,
                        'Start Date': feast.date.strftime('%x'), # not safe, cause it depends on locale # WARNING 
                        'End Date':feast.date.strftime('%x')}
                writer.writerow(data)
    csv_file.close()
    return True # return file as string ? as iostream ? TODO



