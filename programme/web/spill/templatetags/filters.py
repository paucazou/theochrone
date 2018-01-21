# This module describes custom template tags
from django.template.defaulttags import register

# Dictionary: access to a value through a key variable
# https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
@register.filter(name="key")
def get_item(dictionary, key):
    """Return a value matching with key in dictionary.
    If key doesn't exist, return a tuple containing the dictionary and a KeyError.
    Usage: {{ dictionary|key:NAME }} where NAME can be a variable
    WARNING no space are allowed between the name of the dictionary and the key"""
    return dictionary.get(key,(dictionary,KeyError(key)))

@register.filter(name="defkey")
def defkey(returned_value, default):
    """Takes the return value of get_item function (see above). 
    If returned_value contains an error, return the value matching with key in default.
    Usage: {{ dictionary|key:NAME|defkey:DEFAULT }}
    Please be careful to spaces
    Useful if defkey is a variable and not a litteral string"""
    if isinstance(returned_value,tuple) and isinstance(returned_value[1],KeyError):
        dictionary, returned_value = returned_value 
    return returned_value if not isinstance(returned_value,KeyError) else dictionary.get(default)
