import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from build_database import db, band
from utilities import shredTTOTMs
import urllib.request, json, getopt
from bs4 import BeautifulSoup
from build_database import band
import random
from sqlalchemy.sql.expression import func
from random import shuffle

def get_jukebox_bangers():
    url = 'http://www.thesinglesjukebox.com/?p=25856'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")

    a = bs.find('li', {'id': 'linkcat-215'})
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

    socket.setdefaulttimeout(15)
    # creation of the SQL database and the "session" object that is used to manage
    # communications with the database
    engine = create_engine('sqlite:///../../databases/scout.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    session = Session()

    playlist_name = 'KEXP charts'
    tracks = session.query(band).filter(band.source == playlist_name).order_by(func.random())
    for i in tracks[:999]:
        print (i.song, i.id)
    print (tracks.count())

    a = list(range(0,10))
    print (shuffle(a))
    print (a)
