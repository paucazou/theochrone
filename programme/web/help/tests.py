from django.test import TestCase
from .views import _populate, HelpArticle
import help.views
import unittest.mock as mock


class MagicModel:
    """Mocks the HelpArticle class"""
    def __init__(self,children=None):
        self.Children = mock.MagicMock()
        self.Children.defer().filter.return_value = children

# Create your tests here.

class PopulateTests(TestCase):
    @mock.patch('help.views.HelpArticle.Children.defer("text").filter(published__exact=True')
    def test_populate(self,children_patch):
        children_patch.return_value=[MagicModel()]
        return_value = _populate(model,[])
        print(return_value)

       
