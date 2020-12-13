import sys

sys.path.append("site-packages")
import requests
import cfscrape
import json
import re
import time
from abc import ABCMeta, abstractmethod
import string
from unidecode import unidecode
from urllib import parse
from datetime import datetime
import xml.etree.ElementTree as ET
import uuid
import random
import requests

TRANS_TABLE = {ord(c): None for c in string.punctuation}


# make a class for whatever service anime can be found on
class Source:

    # create meta class for abstract classes that we dont need to use immediately
    __metaclass__ = ABCMeta

    def __init__(self, titleList, seasons, region, proxy):
        self.serviceName = ""
        self.shows = []
        self.titleList = titleList
        self.seasons = seasons
        self.region = region
        self.proxy = proxy

    # if list of shows needs to be updated (optional)
    @abstractmethod
    def updateShows(self, animeList):
        pass

    # data is reserved for each streaming service
    @abstractmethod
    def getData(self):
        pass

    # each show has a name so no need to make this abstract
    def getServiceName(self):
        return self.serviceName

    # add show names to a list
    def addToList(self, animeName, url, animeList):
        # list for names
        animeNames = [animeName]

        # if the name of the show is in our list of shows
        if animeName in self.titleList:
            # store in list
            animeNames[0] = self.titleList[animeName]
        # if the anime titles are in the json file
        if self.serviceName in self.titleList:
            # if passed name is in title list under the big list of shows
            if animeNames[0] in self.titleList[self.serviceName]:
                # if the passed name is an empty string in the list, return
                if self.titleList[self.serviceName][animeNames[0]] == "":
                    return
                # otherwise store corresponding title in the list
                animeNames[0] = self.titleList[self.serviceName][animeNames[0]]
        # if titles are in season json file THIS SHOULD BE OPTIONAL
        if self.serviceName in self.seasons:
            if animeNames[0] in self.seasons[self.serviceName]:
                showNames = animeNames + self.seasons[self.serviceName][animeNames[0]]
        # convert unicode into a unicode string in python
        for name in animeNames:
            translated_name = unidecode(name.lower()).translate(TRANS_TABLE).replace('  ', ' ')
            # if the name is in the passed list, provide url
            if translated_name in animeList:
                animeList[translated_name]['sites'][self.serviceName] = url
            # else make a new entry in the list with name and url
            else:
                show_obj = {'name': name, 'sites': {self.serviceName: url}}
                animeList[translated_name] = show_obj

# make a class for a specific streaming service (crunchyroll)
class CrunchyRoll(Source):

    # define streaming service as "CrunchyRoll"
    def __init__(self, titleList, seasons, region = 'us', proxy = {}):
        Source.__init__(self, titleList, seasons, region, proxy)
        self.serviceName = "crunchyroll"

    # add shows to the list
    def updateShows(self, animeList):
        self.shows = self.getData()
        # if program cant find show
        if not self.shows:
            sys.exit('No shows were found for ' + self.name)
        # Go through the shows in service and add them to the list of anime
        for show in self.shows:
            animeName = unidecode(show[0].strip())
            url = "https://www.crunchyroll.com" + show[1]
            Source.addToList(self, animeName, url, animeList)

    # get the data from streaming service
    def getData(self):
        # open our json file with all of our credentials to streaming service
        with open('streamingCreds.json') as creds:
            # deserialize file object
            login = json.load(creds)
        # create a CloudFareScraper instance with cfscrape so we can bypass CR's anti-bot page
        crunchyRollScrape = cfscrape.create_scraper()
        # parameters to logging in
        parameters = {
            "formname": "RpcApiUser_Login",
            "failurl": "https://www.crunchyroll.com/login",
            "name": login['crunchyroll']['usernameCR'],
            "password": login['crunchyroll']['passwordCR']
        }

        # login to streaming service so we can start searching for anime
        crunchyRollScrape.get('https://www.crunchyroll.com/login', parameters = parameters, proxies = self.proxy)
        crunchyRollScrape.post('https://www.crunchyroll.com/?formhandler', parameters = parameters, proxies = self.proxy)
        # WILL NEED TO CHANGE THIS IN THE FUTURE
        blob = crunchyRollScrape.get('http://www.crunchyroll.com/videos/anime/alpha?group=all', proxies = self.proxy)
        # regex to find shows
        regex = '<a title=\"([^\"]*)\" token=\"shows-portraits\" itemprop=\"url\" href=\"([^\"]*)\"'
        return re.findall(regex, blob.text)


