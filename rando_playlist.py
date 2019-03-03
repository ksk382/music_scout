# -*- coding: utf-8 -*-
from gsheetpull import sheetpull
import urllib.request, json, getopt
import datetime as dt
from bs4 import BeautifulSoup
from build_database import band


def get_npr_songs():
    page_num = 1
    url = 'https://www.npr.org/2018/12/05/671206143/the-100-best-songs-of-2018-page-1'
    for i in range(1, 6):
        print (url)
        print('NPR page: {0}'.format(i))
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=hdr)
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
        l = soup.find('div', {'id':'res672080372'})
        m = l.find('b')
        print (m)
        n = m.parent
        print (n)
        o = n.findAll('a')

        print ('o:', '\n\n')
        for i in o:
            print (i)
        input('enter')

        a = soup.findAll('h3', {'class':'edTag'})
        g = []
        for j in a:
            k = j.text
            if k[0] == '\"':
                song = k.strip()[1:-1]
                new_band = band(name = artist, song = song, appeared = 'NPR Top 100 Songs')
                g.append(new_band)
            else:
                artist = k.strip()


    for k in g:
        print (k.name, k.song)

    print (len(g))

    return g



if __name__ == "__main__":
    print ('hello')
    get_npr_songs()