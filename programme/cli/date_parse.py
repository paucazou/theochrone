#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
"""Parse one or two strings and return a tuple of datetime.date"""
"""This module will be renamed dateparse when finished"""
# Special thanks to Ruslan Spivak and his wonderful LSBASI series ! https://ruslanspivak.com/lsbasi-part1/

import calendar
import collections
import datetime
import messages
import re
import words2num
TimeSpan = collections.namedtuple('TimeSpan',('start','stop'))
cal = calendar.Calendar()
# Lexer part

## Token types

class KeyWords:
    """A simple struct of keywords available for each language"""
    EOF = 'EOF'

    def __init__(self):
        self.INTEGER = [r"\d+"]
        self.SEP = ['/',':','-']

    def __iter__(self):
        """Iterates over the dict"""
        for type, values in self.__dict__.items():
            for value in values:
                yield type, re.compile(value)
        #yield 'WORD', self.WORD


english_keywords = KeyWords()
english_keywords.MONTH = [ month.lower() for month in messages.MessagesTranslator.months['en'] if month]
english_keywords.WEEKDAY = [ weekday.lower() for weekday in messages.MessagesTranslator.weekdays['en'] if weekday]
english_keywords.DIMINUTIVE = ['st','nd','rd','th']
english_keywords.RELATIVE_PLUS = ['this','day after','tomorrow','next', 'in','after next','coming']
english_keywords.RELATIVE_EQUAL = ['','today']
english_keywords.RELATIVE_MINUS = ['day before','yesterday','previous','ago','before last','past']
english_keywords.LINK = ['and','\\+']
english_keywords.UNIT = ['day','month','year']
english_keywords.USELESS_WORD = ['of','the','s']
english_keywords.WORD_NUMBER = ['first','second','third','fifth','eighth','ninth','twelfth']
english_keywords.WORD_NUMBER.extend( ['zero','a','one','two','three','four','five','six','seven','eight','nine','ten',
        'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty',
        'thirty','forty','fifty','sixty','seventy','eighty','ninety','hundred','thousand','million'])
english_keywords.SEP.append(',')

english_numbers = {word:nb for word,nb in zip(english_keywords.WORD_NUMBER,(
    1,2,3,5,8,9,12,
    0,1,1,2,3,4,5,6,7,8,9,10,
    11,12,13,14,15,16,17,18,19,20,
    30,40,50,60,70,80,90,100,1000,10**6))}

keywords = {
        'en':english_keywords,
        }
numbers = {
        'en':english_numbers,
        }



class Token:
    """A simple token as recognized by the lexer"""

    def __init__(self,type: str, value: str):
        """Set the token"""
        self.type = type
        self.value = value

    def __str__(self):
        """Representation of the class instance"""
        return "Token({} : {})".format(
                self.type, repr(self.value))

    def __repr__(self):
        """Representation of the class instance"""
        return self.__str__()

    def __bool__(self):
        """Bool value of a Token"""
        return self.type


class Lexer:
    """Split words into a list of tokens"""

    def __init__(self, tokens_type, lang='en'):
        """Set the lexer"""
        self.tokens_type = tokens_type
        self.lang = lang
    
    def _error(self,word: str):
        """Raises error for invalid word"""
        raise SyntaxError("Invalid word : {}".format(word))

    def _skip_whitespace(self):
        """Ignore whitespace"""
        while self.stream[self.pos] is not None and self.stream[self.pos].isspace():
            self.pos += 1

    def tokenize(self,string_entered: str) -> list:
        """Return tokens matching with self.lang""" #http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1
        self.pos = 0
        self.stream = string_entered.lower()
        tokens = []
        while self.pos < len(self.stream):
            self._skip_whitespace()
            match = re.match('','')
            for type, regex in self.tokens_type: # regular tokens
                _match = regex.match(self.stream,self.pos)
                if _match and _match.end(0) > match.end(0):
                    match = _match
                    token = Token(type,match.group(0))

            if match.end(0) == 0:
                self._error(self.stream[self.pos:])
            else:
                tokens.append(token)
                self.pos = match.end(0)
        tokens.append(Token(self.tokens_type.EOF,self.tokens_type.EOF))

        return tokens


# Parser
## Nodes
class AST:
    """Main class of nodes"""
    pass

class RelativeNode(AST):
    """A date relative to today"""
    
    def __init__(self, parent=None, sign=None):
        """sign: PLUS, MINUS, EQUAL"""
        self.sign = sign
        self.unit = Unit('day')# Unit
        self.value = Number('1')# number, BinOp, WordNumber
        parent = parent # None or RelativeNode

    def is_full(self) -> bool:
        """Return full if sign,unit and value are set"""
        return self.sign and self.unit and self.value

class Unit(AST):
    """A node with a span equal to day, week, month or year"""

    def __init__(self,value: str):
        """set value"""
        self.value = value

class WordNumber(AST):
    """A node representing a number in words, cardinal or ordinal"""

    def __init__(self,value: str):
        """Set the tokens representing the number"""
        self.value = value 

class BinOp(AST):
    """A node representing a binary operator (+/*)"""

    def __init__(self,sign: str,right: AST,left: WordNumber):
        """Set the node"""
        self.sign = sign
        self.right = right # WordNumber or BinOp
        self.left = left

class Number(AST): # useless per se, but useful because the interpreter will meet Number or BinOp or WordNumber
    """An integer"""

    def __init__(self,value: str):
        """Set the value"""
        self.value = int(value)

class DistanceNode(AST):
    """A node representing a distance"""

    def __init__(self,number,unit: Unit):
        self.number = number # BinOp or Number
        self.unit = unit


class PartialDate(AST):
    """A node representing a date with possible lacks"""
    def __init__(self):
        """Inits the instance"""
        self.nodes = []

    def __len__(self):
        """Length of self.nodes"""
        return len(self.nodes)

    def __contain__(self,node_type):
        """return if a token_type is present in self.nodes"""
        return [node for node in self.nodes if isinstance(node,node_type)]

    def append(self,node: AST):
        """Append node to self.nodes"""
        self.nodes.append(node)

    def expand(self):
        """set attributes to be more readable"""
        for node,name in zip(self.nodes,('first','second','third')):
            setattr(self,name,node)

class WeekDayNode(AST):
    """A node representing a weekday"""
    def __init__(self,value: str):
        """Set the value"""
        self.value = value

class MonthNameNode(AST):
    """A node representing a month in letters"""
    def __init__(self,value: str):
        """Set the value"""
        self.value = value


class Parser:
    """Parse tokens and return an AST"""

    def __init__(self,keywords: KeyWords,lang='en'):
        """Set the parser"""
        self.keywords = keywords
        self.lang = lang

    def _error(self):
        """Raises a syntax error"""
        raise SyntaxError('Invalid syntax : {}'.format(self.current_token.value))

    def _eat(self,*token_type):
        """Compare current token with token
        desired. More than one token_type can be checked.
        Get next token or raise error"""
        if self.current_token.type in token_type:
            self._next_token()
        else:
            self._error()

    def _next_token(self,start=None) -> Token:
        """Set self.current_token
        start may be a list of tokens"""
        if start:
            self.pos = -1
            self.tokens = [token for token in start if token.type not in  ('USELESS_WORD','SEP','DIMINUTIVE') ]
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
        return self.current_token

    def _get_following_token(self,pos=1) -> Token: # probably useless
        """Get the following token but do not 
        increment self.pos"""
        pos = self.pos + pos
        return self.tokens[pos] if pos < len(self.tokens) else Token(None,None)

    def _get_type_and_pos(self,type):
        """Try to get the position of the given type in self.tokens
        If type can't be found, return -1"""
        for i,token in enumerate(self.tokens):
            if token.type == type:
                return i
        else:
            return -1


    def parse(self,tokens: list) -> AST:
        """main method called by the user."""
        self._next_token(start=tokens)

        node = self._date()
        self._eat(self.keywords.EOF)
        
        return node

    def _date(self):
        """date : relative_kw | weekday_special | regular_date"""
        token = self.current_token
        if [token for token in self.tokens if token.type == 'WEEKDAY']:
            node = self._weekday_special()
        elif [token for token in self.tokens if token.type in ('UNIT','RELATIVE_PLUS','RELATIVE_MINUS','RELATIVE_EQUAL')]:
            node = self._relative_kw()
        else:
            node = self._regular_date()

        return node

    def _relative_kw(self): # pas trop mal, mais à revoir pour améliorer la sécurité : il faut qu'on soit sûr qu'une nouvelle valeur n'ait pas été saisie

        node = RelativeNode()
        relative_types = ('RELATIVE_PLUS','RELATIVE_MINUS','RELATIVE_EQUAL')

        while self.current_token.type not in ('EOF','LINK'):
            if self.current_token.type in relative_types:
                node.sign = self.current_token.type.partition('_')[2]
                self._eat(*relative_types)
            if self.current_token.type == 'INTEGER':
                node.value = self._number()
            if self.current_token.type == 'WORD_NUMBER':
                node.value = self._word_number()
            if self.current_token.type == 'UNIT':
                node.unit = self._unit()

        if self.current_token.type == 'LINK':
            _node = self._relative_kw()
            _node.parent = node
            node = _node

        return node

    def _regular_date(self):
        """regular_date : six_or_eight_digits |"""
        token = self.current_token

        if len(token.value) in (8,6) and token.type == 'INTEGER':
            node = self._six_or_eight_digits()
        else:
            methods = {'INTEGER':self._number,
                    'WORD_NUMBER':self._word_number,
                    'MONTH':self._month,
                    }

            node = PartialDate()
            while self.current_token.type != 'EOF':
                node.append(
                        methods[self.current_token.type]()
                        )
        return node

    def _unit(self):
        """return a unit"""
        node = Unit(self.current_token.value)
        self._eat('UNIT')
        return node


    def _month(self):
        """return a MonthNameNode node"""
        node = MonthNameNode(self.current_token.value)
        self._eat('MONTH')
        return node

    def _weekday(self):
        """return a weekday node"""
        node = WeekDayNode(self.current_token.value)
        self.eat('WEEKDAY')
        return node

    def _number(self):
        """Return a Number instance"""
        value = self.current_token.value
        self._eat('INTEGER')
        return Number(value = value)


    def _word_number(self) -> AST:
        """A method managing a word number, returning a WordNumber or a BinOp"""

        node = WordNumber(self.current_token.value)
        self._eat('WORD_NUMBER')

        while self.current_token.type in ('SEP','WORD_NUMBER','LINK'):
            if self.current_token.type in ('SEP','LINK'):
                self._next_token()
                continue
            elif self.current_token.value in ('hundred','thousand','million'):
                sign = 'MUL'
            else:
                sign = 'PLUS'
            node = BinOp(sign,node,WordNumber(self.current_token.value))
            self._eat('WORD_NUMBER')

        return node

    def _six_or_eight_digits(self):
        """Manages a six or eight digits string"""
        raw = re.findall('..',self.current_token.value) # https://stackoverflow.com/questions/9475241/split-string-every-nth-character
        node = PartialDate()
        node.nodes = [Number(elt) for elt in (raw[0],raw[1],''.join(raw[2:])) ]
        self._eat('INTEGER')

        return node

        

# Interpreter

class Interpreter:
    def interpret(self,node: AST,numbers: dict,keywords: KeyWords,lang='en'):
        """This method is called by the user.
        node is a result of the parser.
        numbers are a dict with the numbers in the current language
        and decimal numbers. Ex: {'one':1}
        """

        self.numbers = numbers
        self.keywords = keywords
        self.lang = lang
        self.today = datetime.date.today()
        return self.visit(node)

    def visit(self,node):
        method_name = "visit_{}".format(type(node).__name__)
        visitor = getattr(self,method_name,self.generic_visit)
        return visitor(node)

    def generic_visit(self,node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_RelativeNode(self,node):
        """Visit a node relative to today"""


    def visit_PartialDate(self,node: AST) -> TimeSpan:
        """Visitor of PartialDate node"""
        length = len(node)
        node.expand()

        if length == 1:
            # month, day or year
            if isinstance(node.first,MonthNameNode):
                result = self.fullmonth(self.visit(node.first),self.today.year)
            else:
                nb_result = self.visit(node.first)
                if nb_result < 50:
                    date = self.today.replace(day = nb_result)
                    result = TimeSpan(date,date)
                else:
                    year = self.correct_year(nb_result)
                    result = self.fullyear(year)

        elif length == 2:
            pass # month/year month/day
            first, second = self.visit(node.first), self.visit(node.second)
            if second < 50:
                date = self.today.replace(month=first,day=second)
                result = TimeSpan(date,date)
            else:
                result = self.fullmonth(first,second)
        else:
            year = self.visit(node.third)
            year = self.correct_year(year)
            date = datetime.date(
                    year,
                    self.visit(node.first),
                    self.visit(node.second)
                    )
            result = TimeSpan(date,date)

        return result

    def visit_Number(self,node) -> int:
        """Manages Number node"""
        return node.value

    def visit_WordNumber(self,node) -> int:
        """Manages WordNumber node"""
        return self.numbers[node.value]

    def visit_BinOp(self,node) -> int:
        """Manages BinOp node"""
        if node.sign == "PLUS":
            result = self.visit(node.right) + self.visit(node.left)
        elif node.sign == 'MUL':
            result = self.visit(node.right) * self.visit(node.left)
        return result

    def visit_MonthNameNode(self,node) -> int:
        """Manages MonthNameNode"""
        return self.keywords.MONTH.index(node.value) + 1

    def visit_WeekDayNode(self,node) -> int:
        """Manages WeekDayNode"""
        return self.keywords.WEEKDAY.index(node.value) + 1

    def correct_year(self,year: int) -> int:
        """If a year has only two digits,
        return year with these digits 
        of the current century
        Ex: 99 -> 2099"""
        if year < 100:
            first_letters = str(self.today.year)[:2]
            year = int(
                    first_letters + str(year)
                    )
        return year

    def fullmonth(self,month: int, year: int) -> TimeSpan:
        """Return the first and the last day of a month"""
        return TimeSpan(
                datetime.date(year,month,1),
                datetime.date(year,month,calendar.monthrange(year,month)[1])
                )

    def fullyear(self,year: int) -> TimeSpan:
        """Return a full year"""
        return TimeSpan(
                datetime.date(year,1,1),
                datetime.date(year,12,31)
                )


def parse(stream: str,lang='en',keywords=keywords,numbers=numbers) -> TimeSpan:
    """Convenient function which calls
    the lexer, the parser and the interpreter
    and return the result as a tuple
    """
    keywords = keywords[lang]
    numbers = numbers[lang]

    lexer = Lexer(keywords,lang)
    tokens = lexer.tokenize(stream)

    parser = Parser(keywords,lang)
    node = parser.parse(tokens)
    interpreter = Interpreter()
    return interpreter.interpret(node,numbers,keywords)

    
















