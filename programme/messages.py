#!/usr/bin/python3.5
# -*-coding:Utf-8 -*
"""A file with arparse and i18n"""
import argparse
import gettext
import os
from command_line import args

loc = os.path.dirname(os.path.abspath(__file__)) + '/i18n'
gettext.install('messages',loc)


args = args()

class MessagesTranslator: # TEST
    """This class manages the translation of the messages on the fly.
    Please do not include strings related to the content of the Fete objects themselves"""

    """months = {
                'en':['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                'fr':['', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'],
                }
    weekdays = {
                'en':['','Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                'fr':['','dimanche','lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'],
                }"""


    def __init__(self,langs, lang: str): # TEST
        """langs is a dict with str as keys matching with a gettext.translation"""
        self.current_lang = lang
        self.langs = langs

    def __getattr__(self,attribute: str): # TEST
        """Unsafe way to get a translation.
        Uses the current_lang"""
        real_attribute = '_' + attribute
        if real_attribute not in self.__dict__:
            raise AttributeError("{} doesn't exist".format(attribute))
        realvalue = self.__dict__[real_attribute]

        if real_attribute in ('_current_lang','_langs'):
            return realvalue
        if isinstance(realvalue,dict):
            ret_dict = {key:_(value) for key,value in realvalue.items()}
            return ret_dict

        return _(self.__dict__[real_attribute]) 

    def __setattr__(self,attribute: str,value: str): # TEST
        """Set a value"""
        if attribute.startswith('_'):
            raise AttributeError("Please do not set attributes starting with `_`: {}".format(attribute))
        new_attribute = "_" + attribute
        if new_attribute in self.__dict__ and new_attribute not in ('_current_lang','_langs'):
            raise AttributeError("{} already exists".format(attribute))
        self.__dict__[new_attribute] = value

    def get(self,message: str,lang: str): # TEST
        """return a translation of the message in the requested lang"""
        self.setLang(lang)
        return _(getattr(self,message))

    def markToTranslate(self,value: str,attribute: str) -> str: # TEST
        """Mark a string literal to be translated
        and save it into the object under the attribute name
        `example = MessagesTranslator(langs,lang)
        example.markToTranslate("Praise the Lord, o my heart",'praise')
        print(example.praise) # print Praise the Lord, o my heart`
        Command-line: xgettext -kmarkToTranslate -j -o OUTPUT INPUT"""
        self.__setattr__(attribute,value)
        return value

    def setLang(self,lang: str): # TEST
        """Install 'lang' translation"""
        if lang != self.current_lang:
            self.current_lang = ('en',lang)[lang in self.langs]
            self.langs.get(lang,self.langs['en']).install() # TODO maybe save the translations in a dict when first loaded


def translated_messages(file_name,language=args.langue):
    """Return messages translated as a dict
    filename : string : name of the file which requires translation. May be shared data.
    language : string : which language is required. default : args.langue"""
    ### i18n ###
    languages = {
    'fr' : gettext.translation('messages',loc,languages=['fr']),
    'en' : gettext.translation('messages',loc,languages=['en']),
    'la' : gettext.translation('messages',loc,languages=['la_LA']),
    }

    languages[language].install()

    ### Messages ###
    messages = {}
    messages['theochrone'] = MessagesTranslator(langs=languages,lang=language) # a dict with all the messages used in theochrone.py
    messages['adjutoria'] = {
        _('fr'),
        _('en'),
        _('la'),
        } # a dict with all the messages used in adjutoria.py
    messages['officia'] = { 
            }
    


    dateparse_msg = MessagesTranslator(langs=languages,lang=language)
    io = MessagesTranslator(langs=languages,lang=language)
    feastprinter = MessagesTranslator(langs=languages,lang=language)
    if file_name == "dateparse":
        dateparse_msg.markToTranslate('today','today')
        dateparse_msg.markToTranslate('tomorrow','tomorrow')
        dateparse_msg.markToTranslate('yesterday','yesterday')
        dateparse_msg.markToTranslate('week','week')

    elif file_name == "io":
        io.markToTranslate(': ',"colon")
        io.markToTranslate('Liturgical color: {}. ',"color")
        io.markToTranslate('. ','dot')
        io.markToTranslate('Proper: {}. ','proper')
        io.markToTranslate('Status: {}. ','status')
        io.markToTranslate('Station: {}. ','station')
    elif file_name == "feastprinter":
        f=feastprinter
        #TODO it is possible to enter lists or dicts by doing that:
        # list = (_(elt),_(elt),) or {k:_(v),k:_(v)}. should work. less verbose...
        #weekdays
        feastprinter.markToTranslate('Monday','monday')
        feastprinter.markToTranslate('Tuesday','tuesday')
        feastprinter.markToTranslate('Wednesday','wednesday')
        feastprinter.markToTranslate('Thursday','thursday')
        feastprinter.markToTranslate('Friday','friday')
        feastprinter.markToTranslate('Saturday','saturday')
        feastprinter.markToTranslate('Sunday','sunday')
        feastprinter.weekdays = (
                f.monday,f.tuesday,f.wednesday,
                f.thursday,f.friday,f.saturday,f.sunday)
        #months
        feastprinter.markToTranslate('January','january')
        feastprinter.markToTranslate('February','february')
        feastprinter.markToTranslate('March','march')
        feastprinter.markToTranslate('April','april')
        feastprinter.markToTranslate('May','may')
        feastprinter.markToTranslate('June','june')
        feastprinter.markToTranslate('July','july')
        feastprinter.markToTranslate('August','august')
        feastprinter.markToTranslate('September','september')
        feastprinter.markToTranslate('October','october')
        feastprinter.markToTranslate('November','november')
        feastprinter.markToTranslate('December','december')
        feastprinter.months = ('',f.january,f.february,f.march,f.april,
                f.may,f.june,f.july,f.august,
                f.september,f.october,f.november,f.december)
        #classes
        feastprinter.markToTranslate('First class','class1')
        feastprinter.markToTranslate('Second class','class2')
        feastprinter.markToTranslate('Third class','class3')
        feastprinter.markToTranslate('Fourth class','class4')
        feastprinter.markToTranslate('Commemoration','commemoration')
        feastprinter.classes=('',f.class1,f.class2,f.class3,f.class4,f.commemoration)
        #colors
        feastprinter.markToTranslate('white','white')
        feastprinter.markToTranslate('green','green')
        feastprinter.markToTranslate('black','black')
        feastprinter.markToTranslate('violet','violet')
        feastprinter.markToTranslate('red','red')
        feastprinter.markToTranslate('rose','rose')
        feastprinter.colors={
                'blanc':f.white,
                'vert':f.green,
                'noir':f.black,
                'violet':f.violet,
                'rouge':f.red,
                'rose':f.rose}
        # pal
        feastprinter.markToTranslate('Mass Pro Aliquibus Locis','pal')
        # propers
        feastprinter.propers = {
                'roman'         :feastprinter.markToTranslate('Roman','roman'),
                'brazilian'     :feastprinter.markToTranslate('Brazilian','brazilian'),
                'australian'    :feastprinter.markToTranslate('Australian','australian'),
                'canadian'      :feastprinter.markToTranslate('Canadian','canadian'),
                'english'       :feastprinter.markToTranslate('English','english'),
                'french'        :feastprinter.markToTranslate('French','french'),
                'new_zealander' :feastprinter.markToTranslate('New-Zealander','new_zealander'),
                'polish'        :feastprinter.markToTranslate('Polish','polish'),
                'portuguese'    :feastprinter.markToTranslate('Portuguese','portuguese'),
                'scottish'      :feastprinter.markToTranslate('Scottish','scottish'),
                'spanish'       :feastprinter.markToTranslate('Spanish','spanish'),
                'welsh'         :feastprinter.markToTranslate('Welsh','welsh')}
        # seasons
        feastprinter.seasons = {
                'avent'             :feastprinter.markToTranslate('Season of Advent','advent'),
                'nativite'          :feastprinter.markToTranslate('Christmastide (Season of Christmas)','christmas'),
                'epiphanie'         :feastprinter.markToTranslate('Epiphanytide (Season of Christmas)','epiphany'),
                'apres_epiphanie'   :feastprinter.markToTranslate('Season per annum after Epiphany','post_epiphany'),
                'septuagesime'      :feastprinter.markToTranslate('Season of Septuagesim','septuagesim'),
                'careme'            :feastprinter.markToTranslate('Lent (Season of Lent)','lent'),
                'passion'           :feastprinter.markToTranslate('Passiontide (Season of Lent)','passion'),
                'paques'            :feastprinter.markToTranslate('Eastertide (Season of Easter)','easter'),
                'ascension'         :feastprinter.markToTranslate('Ascensiontide (Season of Easter)','ascension'),
                'octave_pentecote'  :feastprinter.markToTranslate('Octave of Pentecost (Season of Easter)','octave_pentecost'),
                'pentecote'         :feastprinter.markToTranslate('Season per annum after Pentecost','pentecost')}
        #status
        feastprinter.markToTranslate('celebrated','celebrated')
        feastprinter.markToTranslate('can be celebrated or commemorated','celebrated_commemorated')
        feastprinter.markToTranslate('can be celebrated','can_celebrated')
        feastprinter.markToTranslate('commemorated','commemorated')
        feastprinter.markToTranslate('omitted','omitted')
        #temporsanct
        feastprinter.markToTranslate('Temporal','temporal')
        feastprinter.markToTranslate('Sanctoral','sanctoral')
        #transfert
        feastprinter.markToTranslate('Transferred. Original date: {}','transfert')


    messages['dateparse'] = dateparse_msg
    messages['io'] = io
    messages['feastprinter'] = feastprinter
    
    return messages[file_name]

