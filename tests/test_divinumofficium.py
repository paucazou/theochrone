#!/usr/bin/python3
# -*-coding:Utf-8 -*
#Deus, in adjutorium meum intende
import datetime
import urllib.parse as up
import urllib.request as ur


def test_link_to_divinum_officium():
    """Test wether the POST access to Divinum Officium
    works. This does not test the page todivinumofficium.html
    itself.
    This test can be pretty long to perform."""
    today = datetime.date.today()
    date = "{}-{}-{}".format(today.month,today.day,today.year)
    pre_post_data = {
            'date'  : date,
            'lang2' : "french", # french is the only lang requested now
            }
    post_data = up.urlencode(pre_post_data).encode()
    page = ur.urlopen("http://divinumofficium.com/cgi-bin/missa/missa.pl",data=post_data) # only mass for now
    assert page.getcode() == 200
    content = page.read().decode()
    with open("content","w") as f:
        f.write(content)
    assert """<OPTION SELECTED VALUE="French">French</OPTION>""" in content # french for now
    assert """<INPUT TYPE=TEXT NAME=date VALUE="{}" SIZE=10>""".format(date) in content


