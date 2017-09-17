from django.shortcuts import render

# Create your views here.
def main(request): # TODO
    """this view only return the help till a complete
    app is made"""
    titre = "Aide"
    return render(request,'help/whole.html',locals())
