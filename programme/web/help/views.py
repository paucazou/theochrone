from django.shortcuts import get_object_or_404, render
from .models import HelpArticle

# Create your views here.
def main(request): # TODO
    """this view only return the help till a complete
    app is made"""
    root_articles = HelpArticle.objects.filter(Children__isnull=True)
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
    children = model.Children.all()
    tree.append(model)
    for child in children:
        tree = _populate(child,tree)
    if children:
        tree.append('STOP')
    return tree

