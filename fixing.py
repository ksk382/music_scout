# -*- coding: utf-8 -*-
import datetime as dt
import socket
import sys
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from build_database import db, band
from utilities import shredTTOTMs, cleandb
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

choices = ['KCRW']
recency = '2018'

load_other_bands(Session, choices)
print ('shred ttotms')
#a = shredTTOTMs(Session)
#print ('Deleted {0} TTOTM bands'.format(a))
#b = cleandb(Session)
#print ('Deleted {0} repeat tracks'.format(b))
print ('\n\n\n\n\nMaking playlists')
#make_playlists(Session, choices, recency=recency)

