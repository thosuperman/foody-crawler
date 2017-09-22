import requests
import time
import datetime
import os
import csv

class Helper:
    fileName = None

    # Get HTML content from URL
    @staticmethod
    def parseHTML(link):
        try:
            html = requests.get(link)
        except Exception, e:
            time.sleep(1)
            html = requests.get(link)
        return html.content

    # Create directory and file name
    @staticmethod
    def createFileName(file):
        directory = 'Data/'

        if not os.path.exists(directory):
            os.makedirs(directory)

        Helper.fileName = directory + file[:-4] + '.csv'


    # Write data into file
    @staticmethod
    def writeInfo(data):
        if Helper.fileName is None:
            Helper.createFileName()

        with open(Helper.fileName, 'ab') as fp:
            file = csv.writer(fp, delimiter = ',',quoting=csv.QUOTE_MINIMAL)
            file.writerow(data)
