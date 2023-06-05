#!/usr/bin/python3.6
from __future__ import print_function
from urllib.request import urlretrieve

from wand.image import Image

from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
from datetime import datetime

html_page = urllib2.urlopen("https://ocean.dmi.dk/arctic/images/MODIS/CapeFarewell_RIC/")

soup = BeautifulSoup(html_page, 'html.parser')

msg = ''
msg = 'Updated at (utc) ' + str(datetime.now()) + '\n'
print(msg)

for i, link in enumerate(soup.findAll('a', attrs={'href': re.compile("ISKO")})):
    print(link)



"""
    imageLink = 'https://ocean.dmi.dk/arctic/' + link.get('value') + '.pdf'
    print(imageLink)


    filename = "mysite/templates/green_ice/chart_" + str(i) + ".pdf"
    print(filename, imageLink)
    urlretrieve(imageLink, filename)
    msg += 'http://www.dmi.dk' + link.get('href') + '\n'

    with Image(filename=filename) as img:
        with img.convert('png') as converted:
            filenamepng = filename + ".png"
            converted.save(filename=filenamepng)
            print(filename)
        with img.convert('jpg') as converted:
            filenamejpg = filename + ".jpg"
            converted.save(filename=filenamejpg)
            print(filename)

    with Image(filename=filename) as imgsmall:
        imgsmall.resize(int(imgsmall.width/1.5), int(imgsmall.height/1.5))
        print(imgsmall.width, imgsmall.size)
        with imgsmall.convert('png') as converted:
            filenamepng = filename + ".small.png"
            converted.save(filename=filenamepng)
            print(filenamepng, imgsmall.size)
        with imgsmall.convert('jpg') as converted:
            filenamejpg = filename + ".small.jpg"
            converted.save(filename=filenamejpg)
            print(filenamejpg, imgsmall.size)

with open("mysite/templates/icelinks.txt", "w") as f:
    f.write(msg)

"""