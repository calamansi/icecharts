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

## ICE CHARTS VIA REST API
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

    # log filename
    log['ice_chart'][region] = filename

## AUTOMATIC ICE CHARTS
# download latest gif directly
# note: we don't get a corresponding timestamp
latest_url = 'http://ocean.dmi.dk:8080/geoserver/autocharts/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fgif&TRANSPARENT=true&FORMAT_OPTIONS=layout%3AASIPchartlegend&BGCOLOR=0xFFFFFF&LEGEND_OPTIONS=fontAntiAliasing%3Atrue%3Bcolumns%3A2%3Bforcelabels%3Aon&LAYERS=autocharts%3Amostrecent_autochart_group&exceptions=application%2Fvnd.ogc.se_inimage&CRS=EPSG%3A999998&STYLES=&WIDTH=950&HEIGHT=1000&BBOX=1157589.9496888728%2C616410.7946925056%2C1737657.4483729554%2C1227018.8777443292'
localfile = 'latest_ice_auto_East.gif'    
urlretrieve(latest_url, localfile)

## ICEBERG CHARTS
log['iceberg_chart'] = {}

directory = 'http://polarportal.dk/fileadmin/polarportal/icebergs/'

# create filename for today - though the file may or may not exist
today = datetime.now(timezone.utc).strftime('%Y%m%d')
filename = 'iceberg_map_Cape_Farewell_1080_EN_' + today + '_0615.png'
print(filename)

latest_url = directory + filename
localfile = 'latest_iceberg.png'

try:
    # try to download the file
    urlretrieve(latest_url, localfile)
except:
    # file doesn't exist, so latest file is the last one we have
    print('File not found: ' + filename)
    print('Reading latest filename from log.txt')
    with open('log.txt', 'r') as f:
        last_log = json.load(f)
        filename = last_log['iceberg_chart']['Farewell']
        print(filename)
else:
    # downsize and convert to gif
    with Image(filename=localfile) as img:
        img.alpha_channel = 'off'
        img.merge_layers('flatten')
        with img.convert('gif') as converted:
            converted.resize(int(converted.width/1.7), int(converted.height/1.7), filter='sinc')
            converted.save(filename='latest_iceberg_Farewell.gif')

# log filename
log['iceberg_chart']['Farewell'] = filename

## WRITE LOG FILE
log['last_run'] = str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')) + ' UTC'
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
