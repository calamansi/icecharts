#!/usr/bin/python3.6
from __future__ import print_function
from urllib.request import urlretrieve

from wand.image import Image

from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
from datetime import datetime, timezone

## ICE CHART
directory = 'https://ocean.dmi.dk/arctic/images/MODIS/CapeFarewell_RIC/'
html_page = urllib2.urlopen(directory)

soup = BeautifulSoup(html_page, 'html.parser')
latest_filename_ice = soup.findAll('a', attrs={'href': re.compile("ISKO")})[-1].get('href')
print(latest_filename_ice)

latest_url = directory + latest_filename_ice
print(latest_url)

localfile = 'latest_ice.pdf'
urlretrieve(latest_url, localfile)

with Image(filename=localfile) as img:
    img.alpha_channel = 'off'
    img.merge_layers('flatten')
    with img.convert('gif') as converted:
        converted.resize(int(converted.width/1.7), int(converted.height/1.7), filter='sinc')
        converted.save(filename='latest_ice.gif')

## ICEBERG MAP
directory = 'http://polarportal.dk/fileadmin/polarportal/icebergs/'
today = datetime.now(timezone.utc).strftime('%Y%m%d')
latest_filename_iceberg = 'iceberg_map_Cape_Farewell_1080_EN_' + today + '_0615.png'
print(latest_filename_iceberg)

latest_url = directory + latest_filename_iceberg
print(latest_url)

localfile = 'latest_iceberg.png'

try:
    urlretrieve(latest_url, localfile)
except:
    with open('latest_iceberg.txt', 'r') as f:
        latest_filename_iceberg = f.read()
else:
    with Image(filename=localfile) as img:
        img.alpha_channel = 'off'
        img.merge_layers('flatten')
        with img.convert('gif') as converted:
            converted.resize(int(converted.width/1.7), int(converted.height/1.7), filter='sinc')
            converted.save(filename='latest_iceberg.gif')
    with open('latest_iceberg.txt', 'w') as f:
        f.write(latest_filename_iceberg)

## TEXT FILE
with open('latest.txt', 'w') as f:
    f.write('latest_ice.gif:     ' + latest_filename_ice + '\n')
    f.write('latest_iceberg.gif: ' + latest_filename_iceberg + '\n')
    f.write('\n')
    f.write('Last check at:      ' + str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')) + ' UTC\n')
