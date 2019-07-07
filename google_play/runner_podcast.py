# -*- coding: utf-8 -*-
import re
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



def KEXP_runner_list():

    with open('runner_songs.txt', 'r') as f:
        a = f.read().replace('\n', ' ')

    print (a)


    b = re.split(r'\d+\.', a)

    tracklist = []
    for i in b:
        if i != '':
            j = i.split('-')
            print (j)
            artist = j[0].strip()
            track = j[1].strip()
            tracklist.append([artist,track])

    print (tracklist)
    return tracklist

def get_ids(tracklist):
    idlist = []
    for line in tracklist:
        id_ = do_track_query(line)
        idlist.append(id_)
    return idlist

print ('\n\n\n')
#tracklist = KEXP_runner_list()
#idlist = get_ids(tracklist)
#with open('runner_track_ids.txt', 'w') as f:
#    for item in idlist:
#        f.write('{}\n'.format(item))
with open('runner_track_ids.txt', 'r') as f:
    a = f.readlines()
idlist = []
for i in a:
    if i.startswith('T'):
        print (i.strip())
        idlist.append(i.strip())
playlist_id = make_new_playlist('KEXP Running Playlist')
api.add_songs_to_playlist(playlist_id, idlist[:800])
print ('Added {0} songs to playlist'.format(len(idlist[:800])))