from modeltranslation.translator import translator, TranslationOptions
from .models import HelpArticle

class HelpArticleTranslationOptions(TranslationOptions):
    fields = ('title','text','short_description')

translator.register(HelpArticle,HelpArticleTranslationOptions)
