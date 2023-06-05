#!/usr/bin/python3.6
from __future__ import print_function
from urllib.request import urlretrieve

from wand.image import Image

from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
from datetime import datetime

directory = 'https://ocean.dmi.dk/arctic/images/MODIS/CapeFarewell_RIC/'
html_page = urllib2.urlopen(directory)

soup = BeautifulSoup(html_page, 'html.parser')

msg = ''
msg = 'Updated at (utc) ' + str(datetime.now()) + '\n'
print(msg)

latest_filename = soup.findAll('a', attrs={'href': re.compile("ISKO")})[-1].get('href')
print(latest_filename)

latest_url = directory + latest_filename
print(latest_url)

localfile = 'latest.pdf'
urlretrieve(latest_url, localfile)

with Image(filename=localfile) as img:
    img.resize(int(img.width/1.5), int(img.height/1.5))
    with img.convert('gif') as converted:
        converted.save(filename='latest.gif')

with open("latest.txt", "w") as f:
    f.write(latest_filename)