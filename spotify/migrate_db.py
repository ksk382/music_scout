# -*- coding: utf-8 -*-
import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database_old import db as db1, band as band1
from joint_build_database_new import db as db2, band as band2
import pandas as pd
from sqlalchemy.orm.session import make_transient


socket.setdefaulttimeout(10)
# creation of the SQL database and the "session" object that is used to manage
# communications with the database
engine = create_engine('sqlite:///../../databases/scout_new.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
metadata = MetaData(db1)
db1.metadata.create_all(engine)
sess1 = Session()

engine = create_engine('sqlite:///../../databases/scout_new_new.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
metadata = MetaData(db2)
db2.metadata.create_all(engine)
sess2 = Session()

a = sess1.query(band1)
print (a.count())

for i in a:
    n = band2(
        name = i.name,
        song = i.song,
        album = i.album,
        appeared = i.appeared,
        release_year = i.release_year,
        comment = i.comment,
        source = i.source,
        cleanname = i.cleanname,
        dateadded = i.dateadded,
        dateplayed = i.dateplayed,
        google_nid = i.google_nid,
        google_storeID = i.google_storeID,
        spotify_id = i.spotify_id,
        spotify_release_date = i.spotify_release_year,
        found_by_album = i.found_by_album,
        got_rest_of_album = i.got_rest_of_album,

    )
    sess2.add(n)

sess2.commit()



