from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import HelpArticle

class HelpArticleAdmin(TranslationAdmin):
    prepopulated_fields = {
            'slug': ('title_en',),
            }

# Register your models here.
admin.site.register(HelpArticle,HelpArticleAdmin)
