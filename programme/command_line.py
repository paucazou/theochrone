#!/usr/bin/python3
# -*-coding:Utf-8 -*
"""A file for command-line arguments"""

import argparse, gettext, locale, os, sys, unicodedata
gettext.install('command_line','./i18n')

arguments = { # essayer d'ajouter les commandes de DATE
    """A dict whith following tree :
    DEST : {
        'short' : '-r',
        'long' : '--research',
        'help' : 'description for zsh or fish',
        'options' : 'if necessary',
        },
        """
        # Main options
        'TODAY': {
            'short':[],
            'long': ['--'],
            },
        'DEPUIS':{
            'short':[],
            'long' : ['--from'],
            },
        'JUSQUE':{
            'short':[],
            'long' : ['--to'],
            },
        'INVERSE':{
            'short':['-r'],
            'long' : ['--reverse'],
            },
        
        # Print options
        'verbose':{
            'short':['-v'],
            'long' : ['--verbose'],
            },
        'couleur':{
            'short':['-c'],
            'long' : ['--color','--colour'],
            },
        'degre':{
            'short':['-d'],
            'long' : ['--degree'],
            },
        'jour_semaine':{
            'short':['-w'],
            'long' : ['--weekday'],
            },
        'transfert':{
            'short':['-t'],
            'long' : ['--transfert'],
            },
        'temporal_ou_sanctoral':{
            'short':['-s'],
            'long' : ['--temporsanct'],
            },
        'temps_liturgique':{
            'short':['-L'],
            'long' : ['--liturgical-time'],
            },
        'date_affichee':{
            'short':['-D'],
            'long' : ['--print-date'],
            },
        'textes':{
            'short':[],
            'long' : ['--show-texts'],
            },
        'martyrology':{
            'short':['-M'],
            'long':['--show-martyrology'],
            },
        'station':{
            'short':['-I'],
            'long':['--statio'],
            },
        'pal':{
            'short':['-a'],
            'long':['--pal'],
            },
        'langue':{
            'short':['-l'],
            'long' : ['--language'],
            'options': ['fr','en','la'],
            },
        
        # Selection options
        'propre': {
            'short':['-p',],
            'long':['--proper','--rite',],
            'options':['romanus','all',]
            },
        'ordo': {
            'short':['-o'],
            'long':['--ordo'],
            'options':['1962'],
            },
        'plus': {
            'short':['-m'],
            'long':['--more'],
            },
        
        # System options
        'navigateur': {
            'short':['-b'],
            'long':['--browser'],
            },
        'gui':{
            'short':['-g'],
            'long':['--gui'],
            },
        'version': {
            'short':[],
            'long':['--version'],
            },
        'poems': {
            'short':[],
            'long':['--poems'],
            },
        'settings' : {
            'short':[],
            'long' : ['--set'],
            },
        
        # History options
        'historique': {
            'short' : ['-H'],
            'long' : ['--show-history'],
            },
        'entree_historique': {
            'short': ['-S'],
            'long' : ['--select-entry'],
            },
        'suivant': {
            'short': ['-N'],
            'long' : ['--next'],
            },
        'precedent':{
            'short': ['-P'],
            'long': ['--previous'],
            },
        
        # Help
        'help':{
            'short':['-h'],
            'long':['--help'],
            }
        }

class AutoCompleter():
    
    def __init__(self):
        self.options = arguments
        self.options_ = []
        
    def autocomplete(self):
        if 'AUTO_COMPLETE' not in os.environ:
            return
        
        words = os.environ['COMP_WORDS'].split()[1:]
        cword = int(os.environ['COMP_CWORD'])
        
        short_options = set()
        
        for arg in words:
            try:
                if arg[0] == '-' and arg[1] != '-':
                    short_options = short_options.union(set(arg[1:]))
            except IndexError:
                continue
        
        if len(words) > 1:
            blast_one = words[-2]
        else:
            blast_one = False
        if len(words) > 0:
            last_one = words[-1]
        else:
            blast_one = False
            last_one = False
        self.options_ = []
        
        for value in self.options.values():
            if 'options' in value:
                if (last_one in value['long'] or last_one in value['short']) or ((blast_one in value['long'] or blast_one in value['short']) and [True for val in value['options'] if last_one in val and last_one != val]): #BUG il fait choisir deux langues...
                    self.options_ = value['options']
                    break
                    
            for long_one in value['long']:
                if long_one in words:
                    value['long'] = []
                    break
            for short_one in value['short']:
                if short_one[1] in short_options:
                    value['long'] = []
            self.options_ += value['long']
                
        try:
            # curr is the current word, with cword being a 1-based index
            curr = words[cword - 1]
        except IndexError:
            curr = ''
        if self.options_ == []:
            self.options_.append('--')
            
        complete = ' '.join(sorted(filter(lambda x: x.startswith(curr),self.options_)))
        print(complete)
        sys.exit(1)

def default_language():
    """A function which defines default language of the system
    If a language was set default by user, return it"""
    file = os.path.expanduser('~/.theochrone/config/LANG')
    try:
        with open(file) as f:
            return f.read()
    except FileNotFoundError:
        pass
    langue = locale.getdefaultlocale()[0]
    if 'fr' in langue:
        langue = 'fr'
    else:
        langue = 'en'
    return langue

class CoursDeLangue(argparse.Action):
    """A class to set language name entered by user"""
    def __call__(self,parser,namespace,value,option_string=None):
        language_available = { 'fr': (_('francais'),'fr'),
                              'en':('en',_('english')),
                              'la':('la',_('latina'))}
        def sans_accent(mot):
            """Prend des mots avec accents, cédilles, etc. et les renvoie sans, et en minuscules.""" # voir si on ne peut pas le mettre dans officia.
            return ''.join(c for c in unicodedata.normalize('NFD',mot.lower()) if unicodedata.category(c) != 'Mn')
        value = sans_accent(value.lower())
        for key,values in language_available.items():
            if value in values or value == key:
                value = key
                break
        if value not in ('fr','la','en'):
            print(_("Language entered is not available. Default language will be used instead."))
            value = default_language()
        setattr(namespace,self.dest,value)

### Command-line args ###
def args():
    """A function which returns args."""
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
                        - Day in figures, month in letters, year in figures :
                        ex. 30 december 1990 ; 8th july 1990
                        - weekday before the date as above : ex. Wednesday the 24th of January 2017
                        WARNING !!! The order of these elements much depends on your language.
                    - You can imply one of these elements, and so works Theochrone :
                        - a figure between 1 and 31 : day of the current month in the current year
                        - a weekday in letters only : the requested day in the current week
                        (starting with Sunday)
                        - a month only (ex : july, sept,...) : the complete month of the current year
                        - the day and the month without year : current year used
                        - a number between 1600 and 4100 : the complete year.
                        - a word as listed below in your current language :
                            - 'week' : the complete current week, starting with Sunday,
                            ending with Saturday.
                            You can also ask for 'next' or 'last' 'week', which returns the week
                            after current, and the past one.
                            - 'tomorrow' : the day after current one.
                            You can also ask for the 'day after tomorrow'.
                            - 'yesterday' : the day before current one.
                            You can also ask for the 'day before yesterday'.
                            - 'next month', or 'previous month', which returns the month
                            after current one, and the month before current one.
                            - 'next year', or 'previous year', which returns the year
                            after current one, and the year before current one.
                    All of these formats are also accepted by the --from and --to options. (See below)
                        """))
    main.add_argument('--',dest='TODAY',action='store_true',help=_("""Convenient argument for Windows and OS X users.
        Returns results for current date."""))
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
    main.add_argument('-r','--reverse',dest='INVERSE',nargs='*',default=1,help=_("""Alpha. Does not work properly.
        Reverse is to be a way to find and print feast by entering their names as arguments,
        ex : -r Easter, -r 21 Sunday after Pentecost,...
        Every other options are available with this one.
        With -M option, search is done inside the Roman Martyrology"""))

    affichage = parser.add_argument_group(_('Print options'),description=_("Convenient options for printing results"))
    affichage.add_argument('-v','--verbose', help=_("make theochrone more verbose. Equals to -cdstwLD, and more."),action='store_true')
    affichage.add_argument('-c','--color','--colour', dest='couleur', help=_("print liturgical colour"), action='store_true')
    affichage.add_argument('-d','--degree', dest='degre', help=_('print degree of the liturgical feast'), action='store_true')
    affichage.add_argument('-w','--weekday', dest='jour_semaine',help=_('print weekday'),action='store_true')
    affichage.add_argument('-t','--transfert', dest='transfert', help=_('print wether the feast was transfered'), action='store_true')
    affichage.add_argument('-s','--temporsanct',dest='temporal_ou_sanctoral', help=_('print whether the feast belongs to the sanctorum or de tempore'), action='store_true')
    affichage.add_argument('-L','--liturgical-time', dest='temps_liturgique',help=_('print to which liturgical time the feast belongs to'),action='store_true')
    affichage.add_argument('-D','--print-date',dest='date_affichee',help=_('print date'),action='store_true')
    affichage.add_argument(*arguments['pal']['short'],*arguments['pal']['long'],dest="pal",help=_("""Include Pro Aliquibus Locis masses in results."""),action="store_true")
    affichage.add_argument('--show-texts',dest='textes',help=_("""Show mass texts of the day selected.
        Opens the introibo.fr page in a webbrowser.
        Works only with -r/--reverse (three results max) or an only date."""),action='store_true')
    affichage.add_argument(*arguments['martyrology']['short'],*arguments['martyrology']['long'],dest="martyrology",help=_("""Print the Roman Martyrology for period requested.
        With -r/--reverse, search keywords inside Roman Martyrology."""),action='store_true')
    affichage.add_argument(*arguments['station']['short'],*arguments['station']['long'],dest='station',help=_("""if there is a statio, print it"""),action='store_true')
    affichage.add_argument('-l','--language', dest='langue', action=CoursDeLangue, help=_("""choose your language /!\ ONLY FRENCH AVAILABLE /!\ 
        Available languages :
        - French
        - English
        - Latin"""), default=default_language())

    selection = parser.add_argument_group(_('Selection options'),description=_("Options to focus researches"))
    selection.add_argument('-p','--proper','--rite', dest='propre', help=_('select which proper or rite you want to use'),action='store',default='romanus',choices=['romanus','all'])
    selection.add_argument('-o','--ordo', dest='ordo', help=_('select which ordo you want to use'), type=int, action='store',default=1962,choices=[1962])
    selection.add_argument('-m','--more',dest='plus', help=_('used with -r/--reverse, print a more complete list of feasts matching with arguments entered'), action='store_true')
    
    history = parser.add_argument_group(_('History options'),description=_('All about history'))
    history.add_argument(*arguments['historique']['short'],*arguments['historique']['long'],dest='historique', help=_("Print history and exit. With -r/--reverse, print reverse history"),action='store_true')
    history.add_argument(*arguments['entree_historique']['short'],*arguments['entree_historique']['long'],dest='entree_historique',help=_("""Select which entry of the history you want to use again.
        Can be used with --next and --previous."""),default=0,const=1,action='store',type=int,nargs='?')
    NnPenemies = history.add_mutually_exclusive_group()
    NnPenemies.add_argument(*arguments['suivant']['short'],*arguments['suivant']['long'],dest='suivant',help=_("""Research for the next item. Example :
        the last item researched was a the 1st of January ; --next will research for the 2nd of January.
        It works with a week, a month, a year, and an arbitrary period defined with --from/--to.
        You can also specify a number : to take the same example, after the 1st of January,
        --next 2 will research for the 3rd of January.
        If you specify an entry of the history with --select-entry,
        the research will start from this entry, and not from the last one.
        If used with DATE or --from/--to, these options will have no effect.
        Doesn't work with -r/--reverse."""),action='store',default=0,const=1,type=int,nargs='?')
    NnPenemies.add_argument(*arguments['precedent']['short'],*arguments['precedent']['long'],dest='precedent',help=_("""Research for the previous item.
        Works the same way as --next, on the other side. See above.
        Doesn't work with -r/--reverse"""),action='store',default=0,const=1,type=int,nargs='?') # mettre toutes ces options dans un groupe exclusif avec -r/DATE, etc.

    system = parser.add_argument_group(_('System options'), description=_("Other options"))
    system.add_argument("-b","--browser",dest="navigateur",help=_("""Open Theochrone in your default webbrowser. You can pass args but following options are disabled :
        - --from/--to options
        - a complete week
        - a complete year
        - years before 1960, after 2100
        - every print option.
        If one of the previous args was entered, it will not result an error,
        but the program will use default value."""),action="store_true")
    system.add_argument(*arguments['gui']['short'],*arguments['gui']['long'],dest='gui',help=_("""Open Theochrone in a Graphical User Interface (GUI).
        This is the standard behaviour if Theochrone is opened in a file manager.
        You can pass all research types args."""),action='store_true')
    system.add_argument('--version', action='version',version='%(prog)s 0.4.1')
    system.add_argument('--poems',help=_('open O Crux ave Spes Unica'), action='store_true')
    system.add_argument(*arguments['settings']['long'],dest='settings',nargs='?',const='nothing',help=_("""Modify some settings of the program and exits. Following options are available :
        - ON/OFF : set settings and history ON (default) or OFF.
        OFF also deletes all your personal settings and history, if previously set.
        - An integer : set the maximum lines of your history.
        - --language : save the default language you want to use.
        Settings and history can be found in '.theochrone', which is in your personal directory."""))

    return parser.parse_args()
