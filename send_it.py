from utilities import cleandb, cleanup, shredTTOTMs
import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from build_database import db, band
from gmusicapi import Mobileclient
from difflib import SequenceMatcher


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


def similar(a, b):
    a = cleanup(a)
    b = cleanup(b)
    return SequenceMatcher(None, a, b).ratio()


def do_track_query(i):

    artist = i.name
    song = i.song
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
            i.storeID = match
            i.storeID_year = release_year
            return i
        else:
            i.storeID = 'failed'
    except Exception as e:
        print (str(e))
        print ('Missed {0}'.format(query))
        i.storeID = 'failed'
        pass

    return i

def do_album_query(i):
    artist = i.name
    album = i.album
    query = ' '.join(i for i in [artist, album])
    res = api.search(query, max_results=50)
    highest = 0
    for result in res['album_hits']:
        r = result['album']
        b1 = r['albumArtist']
        ratio = similar(artist, b1)
        b2 = r['name']
        ratio2 = similar(album, b2)
        prod = (ratio * ratio2)
        if prod > highest:
            match = r['albumId']
            highest = prod

    j = []
    try:
        c = api.get_album_info(match)
        for track in c['tracks']:
            new_track = band(name=i.name,
                             song = track['title'],
                             album = i.album,
                             release_year = i.release_year,
                             appeared = i.appeared,
                             comment = i.comment,
                             source = i.source,
                             cleanname = i.cleanname,
                             dateadded = i.dateadded,
                             dateplayed = i.dateplayed,
                             nid = i.nid,
                             storeID = track['storeId'],
                             storeID_year = track['year'])
            j.append(new_track)

    except:
        print ('No match for {0} - {1}'.format(artist, album))

    return j


def get_ids(Session, source):
    session = Session()
    tracks = session.query(band).filter(band.source == source)
    count = 0
    for i in tracks:
        if i.album is not None and i.song is None and i.storeID != 'album':
            i.storeID = 'album'
            j = do_album_query(i)
            add_count = 0
            for track in j:
                q = session.query(band).filter(band.name == track.name, band.song == track.song)
                if q.first() == None:
                    session.add(track)
                    add_count +=1
            print ('Added {0} tracks from {1} - {2}'.format(add_count, i.name, i.album))
            session.commit()
        if i.storeID is None and i.storeID != 'failed' and i.storeID != 'album':
            i = do_track_query(i)
            session.commit()
            count += 1
    c_str = 'Found IDs for {0} tracks'.format(count)
    return c_str


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
    print('Playlist ID: {0}'.format(playlist_id))

    return playlist_id


def send_it(Session, source, recency):
    session = Session()
    tracks = session.query(band).filter(band.source == source)
    idlist = []
    for i in tracks:
        if i.storeID is not None and i.storeID != 'failed' and i.storeID != 'album':
            if int(i.storeID_year) >= int(recency):
                idlist.append(i.storeID)
    playlist_id = make_new_playlist(source)
    api.add_songs_to_playlist(playlist_id, idlist[:800])
    return


if __name__ == "__main__":

    socket.setdefaulttimeout(10)
    # creation of the SQL database and the "session" object that is used to manage
    # communications with the database
    engine = create_engine('sqlite:///../databases/scout.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    session = Session()

    bandsources = ['KEXP Music That Matters', 'Pitchfork Top Tracks',
                   'Stereogum', 'Metacritic', 'KCRW', 'KEXP playlists',
                   'Pitchfork', 'KEXP charts']

    source = 'KEXP charts'

    #get_ids(Session, source)
    #send_it(Session, source, recency=2018)
