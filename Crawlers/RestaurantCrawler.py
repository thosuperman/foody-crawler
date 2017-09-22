import sys
import os
import csv
import json
import re
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../Functions')

from Functions import *

class RestaurantCrawler:

    # Constructor
    def __init__(self, restaurant):
        url = 'https://www.foody.vn/ho-chi-minh/' + restaurant + '/thuc-don'
        html = Helper.parseHTML(url)
        self.restaurant = restaurant
        self.soup = BeautifulSoup(html, "lxml")

    # Get information from metadata
    def getFromMetadata(self):
        longitude = self.soup.find('meta', property='place:location:longitude')
        latitude = self.soup.find('meta', property='place:location:latitude')
        description = self.soup.find('meta', property='og:description')
        name = self.soup.find('h1')

        data = [
                str(name.text.encode('utf8')),
                latitude['content'],
                longitude['content'],
                str(description['content'].encode('utf8'))
            ]

        return data

    # Get position
    def getPosition(self):
        breadCrumList = self.soup.find('span', {'itemtype': 'http://schema.org/BreadcrumbList'})
        position = breadCrumList.findAll('span', {'itemprop': 'name'})
        address = self.soup.find('a', {'href': '/ho-chi-minh/' + self.restaurant + '/nearBy'})
        streetAddress = address.find('span')

        data = [
            position[0].text.encode('utf8'), # Province
            position[1].text.encode('utf8'), # District
            position[2].text.encode('utf8'), # Area
            streetAddress.text.encode('utf8') # Street Address
        ]

        return data

    # Get times open and close
    def getTimesopen(self):
        timesOpen = self.soup.find('div', {'class': 'micro-timesopen'})
        time = timesOpen.findAll('span')

        if len(time) > 1:
            data = [
                time[4].text, # Open Time
                time[5].text # Close Time
            ]
        else:
            data = ['','']

        return data

    # Get menu
    def getMenu(self):
        script = self.soup.find('script', text=re.compile('window\.intMenu'))
        json_text = re.search(r'^\s*window.\intMenu\s*=\s*({.*?})\s*;\s*$',
            script.string, flags=re.DOTALL | re.MULTILINE).group(1)

        data = [
            json_text.encode('utf8')
        ]

        return data

    # Crawling Handler
    def crawl(self):
        data = []
        dataMetadata = self.getFromMetadata()
        dataPosition = self.getPosition()
        dataTimesopen = self.getTimesopen()
        dataMenu = self.getMenu()

        data.extend(dataMetadata)
        data.extend(dataPosition)
        data.extend(dataTimesopen)
        data.extend(dataMenu)
        Helper.writeInfo(data)
