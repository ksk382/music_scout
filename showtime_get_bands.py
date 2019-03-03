# -*- coding: utf-8 -*-
from gsheetpull import sheetpull
import urllib.request, json, getopt
import datetime as dt
from bs4 import BeautifulSoup
from build_database import band
from pytz import timezone
import socket
from selenium import webdriver
import re
from random import shuffle

def get_TTOTM_bands():
    TTOTMbands = sheetpull()
    print(('{0} total TTOTM tracks'.format(len(TTOTMbands))))
    return TTOTMbands

def Pitchfork_charts(maxbands):
    c = []
    allbands = []
    i=0
    while (len(allbands) < maxbands) and (i<20):
        i = i+1
        try:
            print(('Pitchfork page: {0}'.format(i)))
            site = 'http://pitchfork.com/reviews/best/albums/?page=' + str(i)
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(site, headers=hdr)
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
            a = soup.findAll("ul", {"class": "artist-list"})
            print(("Page {0} retrieved".format(i)))
            for banddiv in a:
                album = banddiv.findNext("h2").text
                newband = band(name=banddiv.text, appeared='Pitchfork 8.0+ reviews', album = album)
                allbands.append(newband)
        except Exception as e:
            print (str(e))
            print(("Page {0} failed".format(i)))
            continue

    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]


def pfork_tracks(maxbands):
    c = []
    allbands = []
    i = 0
    while (len(allbands) < maxbands) and (i < 50):
        i = i + 1
        try:
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
                print (artist, track)
                newband = band(name=artist, appeared='Pitchfork Top Tracks',
                               song=track)
                allbands.append(newband)
        except Exception as e:
            print (str(e))
            print(("Page {0} failed".format(i)))
            continue

    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]

def MTM(maxbands):

    url = 'http://feeds.kexp.org/kexp/musicthatmatters'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")

    allbands = []
    maxbands = 200
    c = []

    for item in bs.findAll('item'):
        if len(allbands) <= maxbands:
            desc = item.find('description').text
            tr = False
            s = ''
            n = []

            for g in range(0, len(desc)):
                if desc[g].isdigit():
                    if desc[g + 1].isdigit() or desc[g + 1] == '.':
                        tr = False
                        if len(s) > 0:
                            n.append(s)
                        s = ''
                if desc[g] == '.':
                    if desc[g - 1].isdigit():
                        tr = True
                if tr == True:
                    s = s + desc[g]

            for i in n:
                h = i[2:].strip().split('<')[0]
                egg = h.split('-')
                if len(egg) < 2:
                    egg = h.split('–')
                if len(egg) < 2:
                    egg = h.split('-')

                try:
                    artist = egg[0].strip()
                    song = egg[1].strip()
                    newband = band(name=artist, appeared='KEXP Music That Matters',
                                   song=song)
                    allbands.append(newband)
                except Exception as e:
                    print (str(e))
                    try:
                        print (h)
                    except:
                        print('unprintable')
                    continue

    for j in allbands:
        if j not in c:
            c.append(j)

    for i in c[:maxbands]:
        print (i.name, i.song)

    return c[:maxbands]


def metacritic(maxbands):

    socket.setdefaulttimeout(15)
    url = 'http://www.metacritic.com/browse/albums/score/metascore/year/filtered'

    chromeOptions = webdriver.ChromeOptions()
    prefs = {'profile.managed_default_content_settings.images': 2}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.get(url)

    innerHTML = driver.execute_script("return document.body.innerHTML")
    bs = BeautifulSoup(innerHTML, 'html.parser')

    driver.quit()
    allbands = []

    a = bs.find('div', {'class': 'product_rows'})
    b = a.find_all('div', {'class': 'product_row release'})
    for i in b:
        artist = i.find('div', {'class': 'product_item product_artist'}).text.strip()
        album = i.find('div', {'class': 'product_item product_title'}).text.strip()
        newband = band(name=artist, appeared='Metacritic', album = album)
        allbands.append(newband)

    c = []
    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]


def sgum(maxbands):

    socket.setdefaulttimeout(10)
    allbands = []
    url1 = 'https://www.stereogum.com/category/franchises/album-of-the-week/'

    j = 1
    while len(allbands) < maxbands:
        print ('Getting Stereogum Album of the Week, page {0}'.format(j))
        url = url1 + 'page/' + str(j) + '/'

        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.get(url)

        innerHTML = driver.execute_script("return document.body.innerHTML")
        bs = BeautifulSoup(innerHTML, 'html.parser')

        driver.quit()

        a = bs.find_all('h2')
        for i in a:
            if 'Album Of The Week:' in i.text:
                b = re.sub('Album Of The Week:', '', i.text)
                c = i.find('em')
                if c == None:
                    c = i.find('i')
                album = c.text.strip()
                artist = re.sub(album, '', b).strip()
                newband = band(name=artist, appeared='Stereogum', album=album)
                allbands.append(newband)

        j+=1
        print ('Found {0} bands so far'.format(len(allbands)))

    c = []
    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]


def KEXP_charts(maxbands):

    allbands = []

    basesite = 'http://kexp.org/charts/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(basesite, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")

    for heading in bs.findAll('h4'):
        genre = heading.text.strip()[:-1]
        print (genre)
        contents = (heading.findNext('p').text).splitlines()
        for i in contents:
            if i == []:
                print ('empty')
                continue
            elif len(i) > 1:
                a = i
                b = a.split()
                if b[0][0].isdigit():
                    b.remove(b[0])
                e = ' '.join(i for i in b)
                e = e.replace('(self-released)', '')
                # print (c)
                d = e.split('-')
                if len(d) == 2:
                    artist = d[0]
                    parens = d[1].find('(')
                    album = d[1][:parens].strip()
                d = e.split('–')
                if len(d) == 2:
                    artist = d[0].strip()
                    parens = d[1].find('(')
                    album = d[1][:parens].strip()

                print (artist, album)
                newband = band(name=artist, appeared=genre, album=album)
                allbands.append(newband)

    # half of this list will be the Top 90
    d = []
    e = []
    for i in allbands:
        if i.appeared == 'KEXP Top 90':
            if i not in d:
                d.append(i)
        else:
            if i not in e:
                e.append(i)

    half = maxbands // 2
    d = d[:half]
    shuffle(e)
    c = d + e[half:maxbands]

    return c[:maxbands]


def KCRW_harvest(maxbands):
    c = []
    i = 1
    allbands = []
    print ('Grabbing KCRW bands')
    while (i<20) and len(allbands)<maxbands:
        url = 'https://tracklist-api.kcrw.com/Simulcast/all/' + str(i)
        response = urllib.request.urlopen(url).read()
        data = json.loads(response)
        print(("KCRW page {0} \n".format(i)))
        for entry in data:
            bandname = entry["artist"]
            trackname = entry['title']
            if entry["program_title"] == "Morning Becomes Eclectic":
                if bandname != "[BREAK]":
                    newband = band(name=bandname, song=trackname, appeared = 'KCRW Eclectic')
                    allbands.append(newband)
        i+=1

    for j in allbands:
        if j not in c:
            c.append(j)

    return c[:maxbands]

def get_jukebox_bangers():
    url = 'http://www.thesinglesjukebox.com/?p=25856'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")

    a = bs.find('li', {'id': 'linkcat-215'})
    print (a.text)
    b = a.findAll('a')
    links = []
    for i in b:
        print (i.text)
        print (i['href'])
        links.append (i['href'])

    adds = []
    for link in links:
        url = link
        req = urllib.request.Request(url, headers=hdr)
        page = urllib.request.urlopen(req)
        bs = BeautifulSoup(page, "html.parser")
        c = bs.find('div', {'class': 'post'})
        d = c.find('h2')
        e = d.text.split('–')
        artist = e[0].strip()
        song = e[1].strip()
        print (artist, song)
        newband = band(name=artist, appeared='Singles Jukebox 2018 Bangers', song = song, )
        adds.append(newband)

    return adds

if __name__ == "__main__":

    MTM(100)