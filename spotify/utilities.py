# -*- coding: utf-8 -*-
import datetime as dt
import unicodedata
import re
from gsheetpull import sheetpull
from joint_build_database_new import band

def cleandb(Session):
    session = Session()
    # delete repeats of storeID
    all_songs = session.query(band).order_by(band.id.desc())
    j = []
    k = []
    for i in all_songs:
        if i.spotify_id not in j:
            j.append(i.spotify_id)
        elif i.spotify_id != 'failed' and i.spotify_id != 'album' and i.spotify_id is not None:
            k.append(i.spotify_id)
            session.delete(i)
    session.commit()

    return len(k)

def shredTTOTMs(Session):
    TTOTMlist = sheetpull()
    session = Session()
    delete_count = 0
    for tband in TTOTMlist:
        name = cleanup(tband[0])
        bands = session.query(band).filter(band.cleanname == name)
        gigs = session.query(gig).filter(gig.cleanname == name)
        for i in bands:
            session.delete(i)
            session.commit()
            delete_count += 1
        for i in gigs:
            session.delete(i)
            session.commit()
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