# -*- coding: utf-8 -*-
import datetime as dt
import unicodedata
import re
from gsheetpull import sheetpull
from joint_build_database_new import band

def cleandb(Session):
    shredTTOTMs(Session)
    session = Session()
    # delete repeats of storeID
    all_songs = session.query(band).order_by(band.id.desc())
    j = []
    k = []
    c = 0
    for i in all_songs:
        c +=1
        if i == None:
            print (c)
            input('nonetype here')
            continue
        if i.spotify_id not in j:
            j.append(i.spotify_id)
        elif i.spotify_id != 'failed' and i.spotify_id != 'album' and i.spotify_id is not None:
            k.append(i.spotify_id)
            session.delete(i)
    session.commit()
    delete_christmas_tracks(Session)
    return len(k)


def delete_christmas_tracks(Session):
    #get rid of anything that played in december
    print ('Deleting any December tracks')
    session = Session()
    a = session.query(band)
    for i in a:
        if i.dateplayed is not None:
            b = dt.datetime.strptime(i.dateplayed, '%Y-%m-%d')
            if b.month == 12:
                session.delete(i)
    session.commit()


def shredTTOTMs(Session):
    TTOTMlist = sheetpull()
    session = Session()
    delete_count = 0
    for tband in TTOTMlist:
        name = cleanup(tband[0])
        bands = session.query(band).filter(band.cleanname == name)
        for i in bands:
            session.delete(i)
            session.commit()
            delete_count += 1
    return delete_count

def cleanup(name):
    #this one strips spaces
    name = cleanish(name)
    cleanname = ''.join(e for e in name if e.isalnum())
    return cleanname

def cleanish(name):
    #this one leaves in the spaces
    #name = name.encode('utf-8')
    badwords = ['and ', 'the ', 'The ', '& ', '’', 'w/ ', '/']
    for word in badwords:
        name = re.sub(word, '', name)
    c = name
    #name = str(c.decode('utf-8'))
    cleanishname = ''.join(c for c in unicodedata.normalize('NFKD', name) if unicodedata.category(c) != 'Mn')
    cleanname = cleanishname.lower().rstrip().lstrip()
    return cleanname

def clean_the_tracks(tracks):
    cleantracks = []
    for i in tracks:
        combo = []
        for j in i:
            a = cleanup(j)
            combo.append(a)
        cleantracks.append(combo)
    return cleantracks