# -*- coding: utf-8 -*-
from gsheetpull import sheetpull
import urllib.request, json, getopt
import datetime as dt
from bs4 import BeautifulSoup
from build_database import band
from gmusicapi import Mobileclient
import os
from difflib import SequenceMatcher
from utilities import cleanup


def get_creds():
    cwd = os.getcwd()
    dirlist = os.listdir(cwd)
    foundpath = False
    for i in dirlist:
        if 'client_secret_' in i:
            with open(i, 'r') as f:
                client_secret_pathname = f.readline().rstrip()
            foundpath = True
    if foundpath:
        i = 'gmusic_creds'
        fname = client_secret_pathname + i
        with open(fname) as f:
            content = f.readlines()
    else:
        print('Failed to find pathname')

    return content

content = get_creds()

print('Logging into Google Music.')
api = Mobileclient()
api.login(content[0], content[1], Mobileclient.FROM_MAC_ADDRESS)
print (api.is_authenticated())

def make_new_playlist(pname):

    playlist_name = pname
    allcontents = api.get_all_user_playlist_contents()

    for i in allcontents:
        if i['name'] == playlist_name:
            playlist_id = i['id']
            print('Deleting old playlist {0}'.format(playlist_name))
            api.delete_playlist(playlist_id)

    print('Creating playlist {0}'.format(playlist_name))
    playlist_id = api.create_playlist(playlist_name, description=None, public=False)
    #print('Playlist ID: {0}'.format(playlist_id))
    return playlist_id

def similar(a, b):
    a = cleanup(a)
    b = cleanup(b)
    return SequenceMatcher(None, a, b).ratio()

def do_track_query(i):

    artist = i[0]
    song = i[1]
    query = ' '.join(i for i in [artist, song])
    try:
        res = api.search(query, max_results=50)
        highest = 0
        match = ''
        for result in res['song_hits']:
            r = result['track']
            b1 = r['artist']
            b2 = r['title']
            ratio1 = similar(artist, b1)
            ratio2 = similar(song, b2)
            prod = ratio1 * ratio2
            if prod > highest:
                highest = prod
                match = r['storeId']
                release_year = r['year']
        if match != '':
            print ('Found {0}'.format(query))
            return match
        else:
            i.storeID = 'failed'
    except Exception as e:
        print (str(e))
        print ('Missed {0}'.format(query))
        pass

    return ''

def get_ids(tracklist):
    idlist = []
    for line in tracklist:
        id_ = do_track_query(line)
        idlist.append(id_)
    return idlist

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


def get_acvlub_best_so_far():
    url = 'https://music.avclub.com/the-best-music-of-2019-so-far-1835587350'

    print (url)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    l = soup.findAll('h3')
    g = []

    for i in l:
        try:
            j = i.text
            k = i.em.text
            artist = j.strip(k).split(',')[0]
            song = k = i.em.text
            g.append([artist, song])
        except:
            pass

    return g

def reddit_list():

    url = 'https://www.reddit.com/r/Music/comments/bz1j8b/the_punkrockers_guide_to_surviving_the_summer_of/'

    print (url)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    l = soup.find('ol', {'class':'s1wjcqzz-13 kPrJXs'})
    k = l.findAll('p', {'class': 's1wjcqzz-10 lkEbBw'})
    print (k)
    g= []

    for i in k:
        j = i.text
        print (j)
        try:
            m = j.split('–')
            artist = m[1]
            track = m[0]
            g.append([artist, track])
        except:
            pass

    for i in g:
        print (i)

    return g

def npr_2019_1():
    g = []

    url = 'https://www.npr.org/2019/06/26/734492599/best-songs-of-2019-so-far-page-1'
    print (url)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    k = soup.findAll('h3', {'class': 'edTag'})
    for i in k:
        j = i.text
        try:
            m = j.split(',')
            artist = m[0]
            track = m[1].split('"')[1]
            print (artist, track)
            g.append([artist, track])
        except:
            pass

    for i in g:
        print (i)
    input('enter')

    url = 'https://www.npr.org/2019/06/26/734529446/best-songs-of-2019-so-far-page-2'
    print (url)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    k = soup.findAll('h3', {'class': 'edTag'})
    for i in k:
        j = i.text
        try:
            m = j.split(',')
            artist = m[0]
            track = m[1].split('"')[1]
            print (artist, track)
            g.append([artist, track])
        except:
            pass

    for i in g:
        print (i)
    input('enter')

    input('done with loop')

    return g

def variety():


    url = 'https://www.thrillist.com/entertainment/nation/best-albums-of-2019'
    print (url)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    k = soup.findAll('h2')
    g = []
    for i in k:
        print (i)
        print (i.text)
        album = i.em.text
        print (album)
        artist = i.text.split('by')[1]
        print (artist, album)
        print ('\n\n')
        g.append([artist, album])
    for i in g:
        print (i)

    return g


if __name__ == "__main__":
    print ('hello')

    tracklist = variety()

    '''
    playlist_name = 'Reddit Punk List'
    fname = 'reddit_punk_list.txt'

    print ('Songs found:    ', len(tracklist))
    idlist = get_ids(tracklist)
    with open(fname, 'w') as f:
        for item in idlist:
            f.write('{}\n'.format(item))
    with open(fname, 'r') as f:
        a = f.readlines()
    idlist = []
    for i in a:
        if i.startswith('T'):
            print (i.strip())
            idlist.append(i.strip())
    print ('{0} tracks found'.format(len(idlist)))

    playlist_id = make_new_playlist(playlist_name)
    api.add_songs_to_playlist(playlist_id, idlist[:800])
    print ('Added {0} songs to playlist'.format(len(idlist[:800])))
    '''