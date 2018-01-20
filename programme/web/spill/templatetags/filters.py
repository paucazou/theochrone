# This module describes custom template tags
from django.template.defaulttags import register

# Dictionary: access to a value through a key variable
# https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
@register.filter(name="key")
def get_item(dictionary, key):
    """Return a value matching with key in dictionary.
    If key doesn't exist, return False.
    Usage: {{ dictionary|key:NAME }} where NAME can be a variable
    WARNING no space are allowed between the name of the dictionary and the key"""
    return dictionary, dictionary.get(key,False)

@register.filter(name="defkey")
def defkey(pack, default):
    """Takes a tuple of a dict and a value (pack).
    If value is False, return the value matching with key in default.
    Usage: {{ dictionary|key:NAME|defkey:DEFAULT }}
    Please be careful to spaces
    Useful if defkey is a variable and not a litteral string"""
    dictionary, returned_value = pack
    return returned_value if returned_value else dictionary.get(default)
