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


def KNKX(maxbands):
    socket.setdefaulttimeout(15)
    url = 'https://www.jazz24.org/playlist/'

    #chromeOptions = webdriver.ChromeOptions()
    #prefs = {'profile.managed_default_content_settings.images': 2}
    #chromeOptions.add_experimental_option("prefs", prefs)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    #options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(1)

    iframes = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(iframes[0])

    tracklist = []
    counter = 0
    while counter < 20 and len(tracklist) < maxbands:
        counter +=1
        d = driver.execute_script("return document.body.innerHTML")
        bs = BeautifulSoup(d, 'html.parser')
        b = bs.find_all('div', {'class': 'track_info_box'})
        for i in b:
            track_info = i.find('div', {'class': 'track_info'})
            try:
                track = track_info.find('div', {'class':'track_name clearfix'}).text.title()
                artist = track_info.find('span', {'class': 'track_field_data'}).text.title()
                tracklist.append([artist, track])
                #print (f'{artist} -- {track}')
            except:
                pass

        #time.sleep(2)
        print ('scrolling')
        driver.execute_script("document.getElementById('episodes_container').scrollBy(0,-10000);")
        print (f'songs collected: {len(tracklist)}')


    driver.quit()

    #return
    c = tracklist
    return c[:maxbands]

if __name__ == '__main__':
    c = knkx(2000)

    print (c)