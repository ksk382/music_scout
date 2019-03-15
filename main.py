# -*- coding: utf-8 -*-
import datetime as dt
import socket
import sys
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from build_database import db, band
from utilities import shredTTOTMs, cleanup
from load_kexp_bands import load_kexp_bands
from load_other_bands import load_other_bands
from make_playlists import make_playlists, top_90

socket.setdefaulttimeout(10)
# creation of the SQL database and the "session" object that is used to manage
# communications with the database
engine = create_engine('sqlite:///../databases/scout.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

metadata = MetaData(db)
db.metadata.create_all(engine)

def get_choices():
    session = Session()
    a = session.query(band.source).distinct()
    print ('Number of playlists to make: {0}'.format(a.count()))
    x = 0
    selections = []
    for i in a:
        x += 1
        print ('{0}. - {1}'.format(x, i[0]))
        selections.append([str(x), i[0]])
    print ('00. - all')
    choice = input('Enter playlists to create, each number separated by commas: \n')

    if choice == '00':
        print ('Getting All')
        a = session.query(band.source).distinct()
        b = []
        for i in a:
            b.append(i[0])
        a = b
    else:
        y = [b.strip() for b in choice.split(',')]
        print (y)
        a = []
        for j in y:
            for k in selections:
                if k[0] == j:
                    a.append(k[1])
    print ('Getting: {0}'.format(a))

    return a

if __name__ == "__main__":

    choices = get_choices()
    recency = input('\n\nEnter oldest year to include: \n')
    try:
        print ('\n\n\nload_other_bands\n\n')
        load_other_bands(Session, choices)
        pass
    except:
        pass
    try:
        print ('\n\n\nload_kexp_bands\n\n')
        load_kexp_bands(Session, choices)
        pass
    except:
        pass
    a = shredTTOTMs(Session)
    print ('Deleted {0} TTOTM bands'.format(a))
    print ('\n\n\n\n\nMaking playlists')
    make_playlists(Session, choices, recency=recency)
    #top_90(Session)

