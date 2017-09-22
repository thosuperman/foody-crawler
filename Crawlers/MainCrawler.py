import os

from RestaurantCrawler import RestaurantCrawler

class MainCrawler:

    # Constructor
    def __init__(self, file):
        self.file = file

    # Crawling Handler
    def crawl(self):
        content = open(os.path.join('Locations', self.file), 'r')
        for line in content:
            url = line.split('/')
            restaurant = url[4].rstrip()

            print 'Crawling: ' + restaurant

            crawler = RestaurantCrawler(restaurant)
            crawler.crawl()
