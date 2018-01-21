from django.db import models

# Create your models here.
class HelpArticle(models.Model):
    title = models.CharField(max_length=30)
    parent = models.ForeignKey('self',on_delete=models.CASCADE)
    version_major = models.PositiveSmallIntegerField()
    version_minor = models.PositiveSmallIntegerField()
    version_patch = models.PositiveSmallIntegerField()
    modification_date = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    text = models.TextField() # the text of the article
    short_description = models.CharField(max_length=100)

    def __str__(self):
        return self.title
