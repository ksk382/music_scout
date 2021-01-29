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


def main():
    sp, username = splog_on()
    playlist_id = check_if_playlist_exists(sp, 'December 2020 final cut', username)
    results = sp.user_playlist_tracks(username, playlist_id)
    print (results)
    for i in results['items']:
        print (i)
        print (i['artist'])
        print (i['track']['name'])
        print ('\n\n\n\n')


if __name__ == '__main__':
    main()