from django.test import TestCase
from django.core.urlresolvers import reverse
from kalendarium import views

import datetime

# Create your tests here.

class KalendariumMainTest(TestCase):
    
    def test_home_alone(self):
        """Tests the main page"""
        answer = self.client.get(reverse('accueil'))
        self.assertEqual(answer.status_code, 200)
        today = datetime.date.today()
        date = "{} {} {}".format(today.day,views.officia.mois_lettre(today.month,'francais'),today.year)
        self.assertContains(answer,date)
