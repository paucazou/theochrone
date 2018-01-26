from django.shortcuts import get_object_or_404, render
from .models import HelpArticle

# Create your views here.
def main(request): # TODO
    """This view return the menu of the app and loads the home page of Help"""
    root_articles = HelpArticle.objects.defer('text').filter(Children__isnull=True,published__exact=True)
    tree = [] # list to render
    for elt in root_articles:
        tree = _populate(elt,tree)
    return tree
    
def read(request,id):
    """This view return the content of an article"""
    #UTILISER L'INVERSION D'URL ID + SLUG
    article = get_object_or_404(HelpArticle,id=id)
    return

def _populate(model,tree):
    children = model.Children.defer('text').filter(published__exact=True)
    tree.append(model)
    for child in children:
        tree = _populate(child,tree)
    if children:
        tree.append('STOP')
    return tree

