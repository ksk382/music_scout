# -*- coding: utf-8 -*-
from gsheetpull import sheetpull
import urllib.request, json, getopt
import datetime as dt
from bs4 import BeautifulSoup
from joint_build_database_new import band
from pytz import timezone
import socket
from selenium import webdriver
import re
from random import shuffle
import time
from selenium.webdriver.common.keys import Keys
from joint_spotify_work import splog_on, check_if_playlist_exists
import spotipy
from showtime_get_bands import sgum


def main():

    url = 'https://pitchfork.com/reviews/best/tracks/'
    print(('Pitchfork page: {0}'.format(i)))
    site = 'https://pitchfork.com/reviews/tracks/?page=' + str(i)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(site, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    a = soup.findAll("div", {"class": "track-collection-item__details"})
    print(("Page {0} retrieved".format(i)))
    for banddiv in a:
        artist = banddiv.find('ul', {'class': 'artist-list'}).li.text \
            .strip().replace('”', '').replace('“', '')
        track = banddiv.find('h2', {'class': 'track-collection-item__title'}).text \
            .strip().replace('”', '').replace('“', '')
        print(artist, track)

if __name__ == '__main__':
    main()