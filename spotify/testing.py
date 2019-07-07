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
a = session.query(band).filter(band.spotify_release_year == '')
print (a.count())

count = 0
barmax = a.count()
sp, username = splog_on()
with progressbar.ProgressBar(max_value=barmax, redirect_stdout=True) as bar:
    for i in a:
        if i.spotify_id is None:
            print ('none')
        else:
            if len(i.spotify_id) == 22:
                i = track_info(i, sp)
                print (i.spotify_release_year)
                session.commit()
        count +=1
        bar.update(count)

