# -*- coding: utf-8 -*-
from joint_spotify_work import find_spotify_ids_no_db, \
    find_spotify_ids, find_spotify_ids_choices, \
    track_info, splog_on, do_a_playlist, get_spotify_ids_for_album
from selenium import webdriver
import urllib.request, json, getopt
from bs4 import BeautifulSoup
from collections import defaultdict
import operator
import re
import time
import pickle
import pandas as pd
import os

def pfork_year_end_tracks():

    playlist_name = 'Pitchfork 2020 Review'
    c = []
    allbands = []
    base_site = 'https://pitchfork.com/features/lists-and-guides/best-songs-2020/'
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

def stereogum_year_end_staff_picks():

    c = []
    playlist_name = 'Stereogum Staff Picks 2020'
    base_site = 'https://www.stereogum.com/2109305/2020-best-songs-list/lists/year-in-review/2020-in-review/'
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
                    if y != '':
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

#dj_alex_year_end()
def clean_tracks(tracks):
    print ('inside cleantracks')
    chk_sym = defaultdict(int)

    # this little loop figures out what the member has used to divide artist from track..assuming it's one of
    # the special characters in 'symbol'
    symbol = "~`!@#$%^&*()_-+={}[]:>;',</?*-+—"
    print ('\n\n\n\n')
    print ('starting char scrub')
    print (tracks)
    for track in tracks:
        print (track)
        for i in track:
            if i in symbol:
                chk_sym[i] += 1
    char = max(chk_sym.items(), key=operator.itemgetter(1))[0]
    print (chk_sym)
    print (char)

    track_names = []
    for i in tracks:
        a = i.split(char)
        b = [re.sub(r'[^\w]', ' ', c).strip() for c in a]
        if b != ['']:
            track_names.append(b)
    return track_names

def list_from_list():
    fname = 'tracklist.txt'
    with open(fname, 'r') as f:
        tracks = f.readlines()
    track_names = clean_tracks(tracks)
    print (track_names)
    for i in track_names:
        print (i)
    playlist_name = input('enter playlist name\n:')
    id_list = find_spotify_ids_no_db(track_names)
    do_a_playlist(id_list, playlist_name)

def workout_songs():
    base_site = 'https://www.menshealth.com/entertainment/a28334737/50-best-indie-workout-songs-of-all-time/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(base_site, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    a = soup.findAll('h2')

    track_list = []
    for i in a:
        print (i.text)
        b = i.text[3:].strip('”').strip('"')
        c = b.split('by')
        print (c)
        d = c[1].strip() + ' - ' + c[0].strip()
        print (d)
        track_list.append(d)

    fname = 'tracklist.txt'
    with open(fname, 'w') as f:
        for i in track_list:
            f.write(i)
            f.write('\n')
    f.close()

def kcrw_playlists():

    base_site = 'https://www.kcrw.com/categories/best-new-music'
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(base_site)
    time.sleep(1)

    iframes = driver.find_elements_by_tag_name("iframe")
    print (iframes)
    #input('enter')
    frame_count = 0
    for j in iframes:
        print (frame_count)
        frame_count+=1
        driver.switch_to.frame(j)
        allbands = []
        counter = 0
        d = driver.execute_script("return document.body.innerHTML")
        bs = BeautifulSoup(d, 'html.parser')
        print (bs.prettify())
        input('enter')
        #print ('scrolling')
        #driver.execute_script("document.getElementById('episodes_container').scrollBy(0,-10000);")
        #print (f'songs collected: {len(allbands)}')

        driver.switch_to.default_content()


    driver.quit()

    return

def kexp_countdown_get_links():
    year = '2020'
    site = f'https://www.kexp.org/read/?category={year}-countdown'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(site, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")

    pointers = []
    morepages = True
    while morepages:
        req = urllib.request.Request(site, headers=hdr)
        page = urllib.request.urlopen(req)
        bs = BeautifulSoup(page, "html.parser")
        a = bs.find('div', {'class': 'u-grid-col u-grid-md-col9 u-md-pr3'})
        links = a.findChildren('a')
        morepages = False
        for i in links:
            x = i.text.strip()
            if x.startswith(f'{year} Top'):
                print (x)
                y = 'https://www.kexp.org' + i['href']
                if y not in pointers:
                    pointers.append(y) #..get_attribute('href')
                    morepages = True
        print ('\n\n')
        b = bs.findAll('a', {'class':'RoundedButton'})
        for i in b:
            if i.text.strip().startswith('View'):
                site = 'https://www.kexp.org/read/' + i['href']
                print (site)
        print ('\n\n')
        print (pointers)

    with open('2020_top_ten_links.pickle', 'wb') as handle:
        pickle.dump(pointers, handle)
    print ('Done pickling')

    return pointers

def kexp_countdown_make_playlists():
    with open('2020_top_ten_links.pickle', 'rb') as handle:
        x = pickle.load(handle)
    x = kexp_countdown_get_links()
    albums = []
    hdr = {'User-Agent': 'Mozilla/5.0'}
    for url in x:
        print (url)
        req = urllib.request.Request(url, headers=hdr)
        page = urllib.request.urlopen(req)
        bs = BeautifulSoup(page, "html.parser")
        table = bs.find("table", attrs={"class": "u-mb2"})
        # The first tr contains the field names.
        try:
            headings = [th.get_text() for th in table.find("tr").find_all("th")]
        except:
            continue

        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        for dataset in datasets:
            d = list(dataset)
            for i in d:
                if i[0].lower() == 'artist':
                    artist = i[1]
                if i[0].lower() == 'album':
                    album = i[1]
            print (f'{artist} -- {album}')
            albums.append([artist,album])

    albums_df = pd.DataFrame([])
    for i in albums:
        albums_df = albums_df.append({'artist': i[0], 'album': i[1]}, ignore_index=True)
    albums_df['track_id'] = pd.Series([])
    albums_df.to_csv('albums_df.csv', compression='gzip', index=False)

    return albums

def make_kexp_countdown_playlists():
    albums = kexp_countdown_make_playlists()
    fname = 'albums_df.csv'
    if os.path.isfile(fname):
        albums_df = pd.read_csv(fname, compression='gzip')
    else:
        albums_df = pd.DataFrame([])
        for i in albums:
            albums_df = albums_df.append({'artist':i[0], 'album':i[1]}, ignore_index=True)
        albums_df['track_id'] = pd.Series([])
        albums_df.to_csv('albums_df.csv', compression='gzip', index=False)

    pd.set_option('display.max_rows', 1000)
    print (albums_df)
    input('enter')
    sp, username = splog_on()
    x = albums_df[albums_df['track_id'].isnull()]
    print (x)
    for index, row in x.iterrows():
        artist = row['artist']
        album = row['album']
        print (artist)
        track_ids = get_spotify_ids_for_album(sp, [artist, album])
        delete_row = albums_df[albums_df['artist'] == artist].index
        albums_df = albums_df.drop(delete_row)
        for i in track_ids:
            albums_df = albums_df.append({'artist':artist,
                                          'album': album,
                                          'track_id':i},
                                          ignore_index=True)
    print (albums_df)
    albums_df.to_csv('albums_df.csv', compression='gzip', index=False)
    albums_df = albums_df[albums_df['track_id'].notnull()]
    track_ids = albums_df['track_id'].unique()
    print (track_ids)
    do_a_playlist(track_ids, 'KEXP 2020 countdown')

def paste_list():
    import re

    site = 'https://www.pastemagazine.com/music/best-albums/best-albums-of-2020/#49-ganser-just-look-at-that-sky'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(site, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")

    a = bs.findAll('h2')
    all_tracks = []
    sp, username = splog_on()
    for i in a:
        j = i.text[3:]
        k = re.sub(r'\W+', '', j[:2])
        j = k + j[2:]
        j = j.strip().split(':')
        artist = j[0]
        album = j[1].strip()
        print (j)
        track_ids = get_spotify_ids_for_album(sp, [artist, album])
        for t in track_ids:
            all_tracks.append(t)
        print (f'found {len(track_ids)} tracks. Total: {len(all_tracks)}')
    print (f'pushing {len(all_tracks)} tracks...')
    do_a_playlist(all_tracks, 'Paste top 50')


def delete_label(album):
    a = album
    print (a)
    b = a.split('(')[0].strip()
    print (b)
    return b


def brook_veg():

    with open('bunch_of_albums.txt', 'r') as f:
        x = f.readlines()
    albumlist = []
    for i in x:
        try:
            print (i)
            j = i.split(' - ')
            artist = j[0].strip()
            album = j[1].strip()
            print (f'album: {album} artist: {artist}')
            album = delete_label(album)
            print ('\n\n\n\n')
            albumlist.append([artist,album])
        except:
            pass
    print (albumlist)
    sp, u = splog_on()
    track_id_all = []
    for k in albumlist:
        print (k)
        track_ids = get_spotify_ids_for_album(sp, k)
        track_id_all = track_id_all + track_ids
    print (f'length of track id all: {len(track_id_all)}')
    print (track_id_all)
    do_a_playlist(track_id_all, 'Brooklyn Vegan Rando Top Indie')

def dj_alex():
    with open('bunch_of_albums.txt', 'r') as f:
        x = f.readlines()
    albumlist = []
    for i in x:
        try:
            print (i)
            j = i.split(' - ')
            artist = j[0].strip()
            album = j[1].strip()
            print (f'album: {album} artist: {artist}')
            album = delete_label(album)
            print ('\n\n\n\n')
            albumlist.append([artist,album])
        except:
            pass
    print (albumlist)
    sp, u = splog_on()
    track_id_all = []
    for k in albumlist:
        print (k)
        track_ids = get_spotify_ids_for_album(sp, k)
        track_id_all = track_id_all + track_ids
    print (f'length of track id all: {len(track_id_all)}')
    print (track_id_all)
    do_a_playlist(track_id_all, 'DJ Alex Year End')

def dj_alex_singles():
    url = 'https://www.kexp.org/read/2020/12/23/2020-top-ten-list-spotlight-alex-ruder/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")
    a = bs.findAll('strong')
    for i in a:
        if 'Favorite Singles' in i.text:
            j = i.parent
    k = j.text.split('\n')
    for i in k:
        if i[:2].isdigit():
            print (i[4:])



if __name__ == '__main__':

    #make_kexp_countdown_playlists()
    #paste_list()
    #brook_veg()
    #dj_alex_singles()
    list_from_list()