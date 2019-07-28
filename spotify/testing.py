# -*- coding: utf-8 -*-
import datetime as dt
import socket
import sys
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database_new import db, band
from joint_spotify_work import find_spotify_ids, find_spotify_ids_choices, track_info, splog_on
from get_user_choices import get_user_choices
from get_the_bands import get_the_bands
from make_spotify_playlists import make_spotify_playlists
import progressbar

engine = create_engine('sqlite:///../../databases/scout_new.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
metadata = MetaData(db)
db.metadata.create_all(engine)

session = Session()



sp, username = splog_on()
current_playlists = sp.user_playlists(username)
for playlist in current_playlists['items']:
    link = playlist['external_urls']['spotify']
    if 'Scout' in playlist['name']:
        print (playlist['name'], link)

