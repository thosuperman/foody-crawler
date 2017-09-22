import sys
import getopt

from Crawlers import *
from Functions import *

def main(argv):
    file = ''

    try:
        opts, args = getopt.getopt(argv, 'hvf:', ['file='])
    except getopt.GetoptError:
        print 'FoodyCrawler.py -f <file>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'FoodyCrawler.py -f <file>'
        elif opt == '-v':
            print 'Foody Crawler 1.2'
        elif opt in ('-f', '--file'):
            file = arg
            Helper.createFileName(file)
            crawler = MainCrawler(file)
            crawler.crawl()

    sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])