# -*- coding: utf-8 -*-
import datetime as dt
import socket
import sys
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database_new import db, band
from joint_spotify_work import find_spotify_ids_no_db, find_spotify_ids, find_spotify_ids_choices, track_info, splog_on, do_a_playlist
from get_user_choices import get_user_choices
from get_the_bands import get_the_bands
from make_spotify_playlists import make_spotify_playlists
import progressbar
import pickle
import urllib.request, json, getopt
from bs4 import BeautifulSoup



def pfork_2019_tracks():

    playlist_name = 'Pitchfork 2019 Review'
    c = []
    allbands = []
    base_site = 'https://pitchfork.com/features/lists-and-guides/best-songs-2019/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(base_site, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    a = soup.findAll("div", {"class": "heading-h3"})
    a = soup.findAll('h2')
    for i in a:
        b = i.text.split(':')
        artist = b[0].strip().replace('”', '').replace('“', '')
        song = b[1].strip().replace('”', '').replace('“', '')
        print (artist, song)
        c.append(b)

    track_list = c
    id_list = find_spotify_ids_no_db(track_list)
    do_a_playlist(id_list, playlist_name)

    return


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def stereogum_staff_picks_2019():

    c = []
    playlist_name = 'Stereogum Staff Picks 2019'
    base_site = 'https://www.stereogum.com/2066366/best-songs-of-2019/franchises/2019-in-review/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(base_site, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    a = soup.findAll('strong')
    for i in a:
        j = i.text.split('\n')
        for k in j:
            if is_number(k[:2]):
                m = k[3:]
                b = m.split('–')
                artist = b[0].strip().replace('”', '').replace('“', '')
                song = b[1].strip().replace('”', '').replace('“', '')
                print (artist, song)
                c.append(b)

    track_list = c
    id_list = find_spotify_ids_no_db(track_list)
    do_a_playlist(id_list, playlist_name)


def dj_alex_year_end():
    c = []
    playlist_name = 'Scout DJ Alex Year End'
    base_site = 'https://kexp.org/read/2019/12/19/2019-top-ten-spotlight-dj-alex/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(base_site, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    a = soup.findAll('b')

    j = []
    for i in a:
        if 'SINGLES' in i.text:
            print (i)
            x = i
            while x is not None:
                x = x.findNext('br')
                if x is not None:
                    y = x.nextSibling.strip()
                    if y is not '':
                        j.append(y)
    print (j)
    print ('\n\n\n')
    for k in j:
        # 01. Charli XCX - "Gone (feat. Christine & The Queens)" / "February 2017 (feat. Clairo & Yaeji)" / "Silver
        if is_number(k[:2]):
            k = k[3:]
        b = k.split('-')
        songs = b[1].split('/')
        artist = b[0].strip().replace('”', '').replace('“', '').replace('"','')
        for song in songs:
            song = song.strip().replace('”', '').replace('“', '').replace('"','')
            c.append([artist,song])
            print (f'{artist} - {song}')

    print (c)
    track_list = c
    id_list = find_spotify_ids_no_db(track_list)
    do_a_playlist(id_list, playlist_name)

dj_alex_year_end()