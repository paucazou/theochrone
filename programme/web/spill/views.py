from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

import datetime
import os
import sys

chemin = os.path.dirname(os.path.abspath(__file__))
programme = os.path.abspath(chemin + '/../..')
sys.path.append(programme)
import annus
import officia

lyear = annus.LiturgicalCalendar()
language = 'francais'
# Create your views here.

@xframe_options_exempt
def main(request):
    """The only view used by the whole app.
    Every other function inframe must redirect to this one"""
    return HttpResponse("""<!DOCTYPE html>
<html>
<head></head>
<body>

<div id="demo">
</div>


<script>
function loadDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML =
      this.responseText;
    }
  };
  xhttp.open("GET", "day", true);
  xhttp.send();
}
loadDoc()
</script>

</body>
</html>""")
    return render(request, 'spill/main.html',locals())

def day(request):
    """Returns value for one date"""
    # faire un forms pour la validation
    day = None # on traite les éléments GET
    if not day:
        day = datetime.date.today()
    lyear(day.year)
    data = lyear[day]
    return render(request,'spill/day.html',locals())
    
def create_module(request):
    """A function to help customers
    to create modules for their blogs"""
    pass
