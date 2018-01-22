from django.shortcuts import render

# Create your views here.
def main(request): # TODO
    """this view only return the help till a complete
    app is made"""
    titre = "Aide"
    return render(request,'help/whole.html',locals())

def _populate(model,tree):
    children = model.helparticle_set.all()
    tree.append(model)
    for child in children:
        tree = _populate(child,tree)
    if children:
        tree.append('STOP')
    return tree
