#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende

import PyQt5.QtCore as QC

_ = QC.QCoreApplication.translate

class ReTranslateBox():
    """A class which can contain only items with the retranslateUI function"""
    def __iter__(self):
        """Iters values of  self.__dict__"""
        for value in self.__dict__.values():
            yield value
        
    def __repr__(self):
        """Returns self.__dict__ to be recognized in the interactive interpreter"""
        return str(self.__dict__)
    
    def __setattr__(self,attribute,value):
        """Tests wether the 'value' is an object which has the function retranslateUI in it.
        If it is true, set the 'attribute'. This function should be useless in prod."""
        if 'retranslateUI' in value.__dir__():
            self.__dict__[attribute] = value
        else:
            raise TypeError("""Could not set attribute '{}' : '{}' object doesn't contain any 'retranslateUI' method.""".format(attribute,value))
        
class SuperTranslator():
    """A class which should be inherited by every custom widget class to make an easy translation on the fly."""
    frLocale = QC.QLocale(QC.QLocale.French)
    enLocale = QC.QLocale(QC.QLocale.English)

    def __init__(self):
        """This method only defines a ReTranslateBox object which is called 'W'. This attribute can only store widgets with a 'retranslateUI' method, i.e. from objects which inherit of this class"""
        self.W = ReTranslateBox()
        self.setUtilities()


    def setUtilities(self):
        """Set translated strings that can be used in many places.
        """
        if getattr(self,'parent',False) and getattr(self.parent,"lang",False):
            self.lang = self.parent.lang
            self.setLocale( self.parent.locale())
        elif getattr(self,"locale",False):
            self.lang = self.locale().bcp47Name()# doesn't work if class inherited is not a QWidget
        self.ordinary_numbers_translated0 = (
	    _('SuperTranslator','First'),
	    _('SuperTranslator','Second'),
	    _('SuperTranslator','Third'),
	    _('SuperTranslator','Fourth'),
	    _('SuperTranslator','Fifth'),
	    _('SuperTranslator','Sixth'))
        self.ordinary_numbers_translated1 = ('',) + self.ordinary_numbers_translated0

        self.weekdays_translated0 = (
                _('SuperTranslator','Monday'),
                _('SuperTranslator','Tuesday'),
                _('SuperTranslator','Wednesday'),
                _('SuperTranslator','Thursday'),
                _('SuperTranslator','Friday'),
                _('SuperTranslator','Saturday'),
                _('SuperTranslator','Sunday'))
        self.weekdays_translated1 = ('',) + self.weekdays_translated0

        self.months_translated0 = (
	    _('SuperTranslator','January'),
	    _('SuperTranslator','February'),
	    _('SuperTranslator','March'),
	    _('SuperTranslator','April'),
	    _('SuperTranslator','May'),
	    _('SuperTranslator','June'),
	    _('SuperTranslator','July'),
	    _('SuperTranslator','August'),
	    _('SuperTranslator','September'),
            _('SuperTranslator','October'),
	    _('SuperTranslator','November'),
	    _('SuperTranslator','December'))
        self.months_translated1 = ('',) + self.months_translated0

        self.week_sentence = _("SuperTranslator","{} week of {} {}")#format(number,month,year)

        
    def retranslateUI(self):
        """This method calls every 'retranslateUI' methods of the 'W' attribute.
        This method should be overloaded by every widget which contains
        widgets to be immediately retranslated
        (i.e., which are not custom widgets).
        User shouldn't forget to call this function if necessary in the function itself :
        SuperTranslator.retranslateUI()"""
        self.setUtilities()

        for a in self.W:
            a.retranslateUI()

    def localizedDate(self,**kwargs) -> str:
        """This function return a date
        with local parameters.
        Options allowed:
                - day: datetime.date
                - week: 1..6 (must match with number of weeks in month)
                - month: 1..12
                - year: 1600..4100
        """
        if "day" in kwargs:
            day = kwargs['day']
            weekday = self.weekdays_translated0[day.weekday()]
            month = self.months_translated1[day.month]
            if self.lang == "fr":
                day_nb = day.day if day.day > 1 else "1er"
                return "{} {} {} {}".format(
                        weekday, day_nb, month, day.year)
            else: # en default
                return "{}, {} {}, {}".format(
                        weekday,month,day.day,day.year)

        elif "week" in kwargs:
            return self.week_sentence.format(
                    self.ordinary_numbers_translated1[kwargs['week']],
                    self.months_translated1[kwargs['month']],
                    kwargs['year'])
        elif 'month' in kwargs:
            return "{} {}".format(
                    self.months_translated1[kwargs['month']],
                    kwargs['year'])
        else:
            raise KeyError("No key match with requested arguments")



