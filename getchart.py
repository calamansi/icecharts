#!/usr/bin/python3.6
from __future__ import print_function
from urllib.request import urlretrieve

from wand.image import Image

from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
from datetime import datetime, timezone

directory = 'https://ocean.dmi.dk/arctic/images/MODIS/CapeFarewell_RIC/'
html_page = urllib2.urlopen(directory)

soup = BeautifulSoup(html_page, 'html.parser')
latest_filename = soup.findAll('a', attrs={'href': re.compile("ISKO")})[-1].get('href')
print(latest_filename)

latest_url = directory + latest_filename
print(latest_url)

localfile = 'latest.pdf'
urlretrieve(latest_url, localfile)

with Image(filename=localfile) as img:
    img.alpha_channel = 'off'
    img.merge_layers('flatten')
    with img.convert('gif') as converted:
        converted.resize(int(converted.width/1.7), int(converted.height/1.7), filter='sinc')
        converted.save(filename='latest.gif')

with open('latest.txt', 'w') as f:
    f.write(latest_filename + '\n')
    f.write('\nLast check at ' + str(datetime.now(timezone.utc)) + ' UTC\n')