from django.db import models
VERSION = '0.5.0'

# Create your models here.
class HelpArticle(models.Model):
    title = models.CharField(max_length=30)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,blank=True,null=True)
    version = models.CharField(max_length=len(VERSION),default=VERSION)
    modification_date = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=30)

    text = models.TextField() # the text of the article
    short_description = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    def has_children(self):
        """Return True if instance has related articles"""
        return bool(self.helparticle_set.all())
