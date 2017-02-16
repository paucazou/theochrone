#!/usr/bin/python3
# -*-coding:Utf-8 -*
"""A file for command-line arguments"""

import argparse, gettext, unicodedata, locale
gettext.install('command_line','./i18n')

def default_language():
    """A function which defines default language of the system"""
    langue = locale.getdefaultlocale()[0]
    if 'fr' in langue:
        langue = 'francais'
    else:
        langue = 'english'
    return langue

class CoursDeLangue(argparse.Action):
    """A class to set language name entered by user"""
    def __call__(self,parser,namespace,value,option_string=None):
        language_available = { 'francais': (_('francais'),'fr'),
                              'english':('en',_('english')),
                              'latina':('la',_('latina'))}
        def sans_accent(mot):
            """Prend des mots avec accents, cédilles, etc. et les renvoie sans, et en minuscules."""
            return ''.join(c for c in unicodedata.normalize('NFD',mot.lower()) if unicodedata.category(c) != 'Mn')
        value = sans_accent(value.lower())
        for key,values in language_available.items():
            if value in values or value == key:
                value = key
                break
        setattr(namespace,self.dest,value)

### Command-line args ###
parser = argparse.ArgumentParser(
        prog='Theochrone',
        formatter_class=argparse.RawTextHelpFormatter,
        description=_("""A universal calendar for the Tridentine Mass (i.e. Extraordinary Form of the Roman Rite)"""),
        epilog=_("Please pray God for me."),
        )
main = parser.add_argument_group(_('Main options'), description=_("Main options of the program"))
main.add_argument('DATE', nargs='*',help=_("""Theochrone accepts many formats :
                  - Nothing : current day
                  - A complete date with year, month and day of month, for example as following :
                    - DD MM YYYY
                    - DD-MM-YYYY
                    - DD/MM/YYYY
                    - DDMMYYYY (eight characters required)
                    - Day in figures, month in letters, year in figures : ex. 30 december 1990 ; 8th july 1990
                    - weekday before the date as above : ex. Wednesday the 24th of January 2017
                    WARNING !!! The order of these elements much depends on your language.
                - You can imply one of these elements, and so works Theochrone :
                    - a figure between 1 and 31 : day of the current month in the current year
                    - a weekday in letters only : the requested day in the current week (starting with Sunday)
                    - a month only (ex : july, sept,...) : the complete month of the current year
                    - the day and the month without year : current year used
                    - a number between 1600 and 4100 : the complete year.
                    - a word as listed below in your current language :
                        - 'week' : the complete current week, starting with Sunday, ending with Saturday. You can also ask for 'next' or 'last' 'week', which returns the week after current, and the past one.
                        - 'tomorrow' : the day after current one. You can also ask for the 'day after tomorrow'.
                        - 'yesterday' : the day before current one. You can also ask for the 'day before yesterday'.
                        - 'next month', or 'previous month', which returns the month after current one, and the month before current one.
                        - 'next year', or 'previous year', which returns the year after current one, and the year before current one.
                All of these formats are also accepted by the --from and --to options. (See below)
                    """))
main.add_argument('--from',dest='DEPUIS',nargs='*',default=1,help=_("""With --to option, --from option can be used to point out the beginning of the period you want to print.
                  Arguments accepted have exactly the same format as DATE (see above).
                  --from may be implied : if --to point out a date later than the current day,
                  --from would automatically considered to be the current day ;
                  else, it would be the first of january of the current year.""" ))
main.add_argument('--to',dest='JUSQUE',nargs='*',default=1,help=_("""With --from option, --to option can be used to point out the end of the period you want to print.
                  Arguments accepted have exactly the same format as DATE (see above).
                  --to may be implied : if --from point out a date prior to the current day,
                  --to would automatically considered to be the current day ;
                  else, it would be the 31st of december of the current year."""))
main.add_argument('-r','--reverse',dest='INVERSE',nargs='*',default=1,help=_("""Alpha. Does not work properly. Reverse is to be a way to find and print feast by entering their names as arguments, ex : -r Easter, -r 21 Sunday after Pentecost,... Every other options are available with this one."""))

affichage = parser.add_argument_group(_('Print options'),description=_("Convenient options for printing results"))
affichage.add_argument('-v','--verbose', help=_("make theochrone more verbose. Equals to -cdstwLD, and more."),action='store_true')
affichage.add_argument('-c','--color','--colour', dest='couleur', help=_("print liturgical colour"), action='store_true')
affichage.add_argument('-d','--degree', dest='degre', help=_('print degree of the liturgical feast'), action='store_true')
affichage.add_argument('-w','--weekday', dest='jour_semaine',help=_('print weekday'),action='store_true')
affichage.add_argument('-t','--transfert', dest='transfert', help=_('print wether the feast was transfered'), action='store_true')
affichage.add_argument('-s','--temporsanct',dest='temporal_ou_sanctoral', help=_('print whether the feast belongs to the sanctorum or de tempore'), action='store_true')
affichage.add_argument('-L','--liturgical-time', dest='temps_liturgique',help=_('print to which liturgical time the feast belongs to'),action='store_true')
affichage.add_argument('-D','--print-date',dest='date_affichee',help=_('print date'),action='store_true')
affichage.add_argument('-l','--language', dest='langue', action=CoursDeLangue, help=_("""choose your language /!\ ONLY FRENCH AVAILABLE /!\ 
    Available languages :
    - French
    - English
    - Latin"""), default=default_language())

selection = parser.add_argument_group(_('Selection options'),description=_("Options to focus researches"))
selection.add_argument('-p','--proper','--rite', dest='propre', help=_('select which proper or rite you want to use'),action='store',default='romanus',choices=['romanus','all'])
selection.add_argument('-o','--ordo', dest='ordo', help=_('select which ordo you want to use'), type=int, action='store',default=1962,choices=[1962])
selection.add_argument('-m','--more',dest='plus', help=_('used with -r/--reverse, print a more complete list of feasts matching with arguments entered'), action='store_true')

system = parser.add_argument_group(_('System options'), description=_("Other options"))
system.add_argument('-b','--browser',dest='navigateur',help=_("Open Theochrone in your default webbrowser. You can pass args but following options are disabled :
    - --from/--to options
    - a complete week
    - a complete year
    - years before 1960, after 2100
    - every print option.
    If one of the previous args was entered, it will not result an error, but the program will use default value."),action='store_true')
system.add_argument('--version', action='version',version='%(prog)s 0.1')
system.add_argument('--test',help='Do not run',action='store_true')
system.add_argument('--poems',help=_('open O Crux ave Spes Unica'), action='store_true')

args = parser.parse_args()
