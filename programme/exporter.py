#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""This module is intented to export
Theochrone results into other formats, such as csv,
in order to be used in other softwares"""
import annus
import csv

def to_csv(start: int,stop: int,file_path: str,lang: str) -> bool:
    """Turn data into a csv file from year start to year stop.
    Return True"""
    # formatting csv writer
    fields = ['Subject','Description','Start Date','End Date']
    csv_file = open(file_path,'w',newline='')
    writer = csv.DictWriter(csv_file,fieldnames=fields)
    writer.writeheader()
    # collecting data
    liturgycal = annus.LiturgicalCalendar()
    liturgycal(start,stop)
    # writing data
    for day in liturgycal:
        for feast in day:
            description = "Add more info"#TODO
            data = {'Subject':feast.nom[lang],
                    'Description':description,
                    'Start Date': feast.date.strftime('%x'), # not safe, cause it depends on locale # WARNING 
                    'End Date':feast.date.strftime('%x')}
            writer.writerow(data)
    return True



