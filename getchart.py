#!/usr/bin/python3.6
from __future__ import print_function
from urllib.request import urlretrieve

from wand.image import Image

from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import json
from datetime import datetime, timezone

log = {}

## ICE CHART VIA REST API
log['ice_chart'] = {}

directory = 'https://www.dmi.dk/dmidk_byvejrWS/rest/icemaps/pdf/'
for region in ['Farewell', 'East', 'Greenland']:
    # get latest colour chart for the region
    query = 'https://www.dmi.dk/dmidk_byvejrWS/rest/icemaps/list/' + region + '/Colour/1'
    html_page = urllib2.urlopen(query)
    soup = BeautifulSoup(html_page, 'html.parser')
    data = json.loads(soup.get_text())
    filename = data[0]['filename']
    print(filename)
    log['ice_chart'][region] = filename

    # download PDF
    latest_url = directory + filename
    localfile = 'latest_ice.pdf'    
    urlretrieve(latest_url, localfile)

    # downsize and convert to gif
    with Image(filename=localfile) as img:
        img.alpha_channel = 'off'
        img.merge_layers('flatten')
        with img.convert('gif') as converted:
            converted.resize(int(converted.width/1.7), int(converted.height/1.7), filter='cubic')
            converted.save(filename='latest_ice_' + region + '.gif')

## ICEBERG MAP
log['iceberg_chart'] = {}

directory = 'http://polarportal.dk/fileadmin/polarportal/icebergs/'
today = datetime.now(timezone.utc).strftime('%Y%m%d')
filename = 'iceberg_map_Cape_Farewell_1080_EN_' + today + '_0615.png'
print(filename)

latest_url = directory + filename
localfile = 'latest_iceberg.png'

try:
    urlretrieve(latest_url, localfile)
except:
    print('Reading log.txt')
    with open('log.txt', 'r') as f:
        last_log = json.load(f)
        filename = last_log['iceberg_chart']['Farewell']
        print(filename)
else:
    log['iceberg_chart']['Farewell'] = filename
    with Image(filename=localfile) as img:
        img.alpha_channel = 'off'
        img.merge_layers('flatten')
        with img.convert('gif') as converted:
            converted.resize(int(converted.width/1.7), int(converted.height/1.7), filter='sinc')
            converted.save(filename='latest_iceberg_Farewell.gif')


## WRITE LOG FILE
log['last_check'] = str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')) + ' UTC'
print(log)
with open('log.txt', 'w') as f:
    f.write(json.dumps(log, indent=4))



"""
## ICE CHART FROM ARCHIVE
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
"""
