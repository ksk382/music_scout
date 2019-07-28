# -*- coding: utf-8 -*-
import datetime as dt
import socket
import sys
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database_new import db, band
from joint_spotify_work import find_spotify_ids, find_spotify_ids_choices, get_spotify_ids
from get_user_choices import get_user_choices
from get_the_bands import get_the_bands
from make_spotify_playlists import make_spotify_playlists
from sqlalchemy import or_
from utilities import cleandb

def clear_failed_2s(Session):

    session = Session()
    a = session.query(band).filter(band.spotify_id=='failed 2')
    print (a.count())
    for i in a:
        i.spotify_id = None
    session.commit()
    input('cleared all the failed 2s')


if __name__ == '__main__':
    engine = create_engine('sqlite:///../../databases/scout_new.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    #clear_failed_2s(Session)

    # get user input--which shows to make playlists for
    choices = get_user_choices(Session)
    recency = input('\n\nEnter oldest year to include: \n')

    # find some bands
    #get_the_bands(Session, choices)

    # insert album tracks for album listings
    #get_album_tracks(Session)

    # get the spotify IDs for them
    get_spotify_ids(Session, choices)

    # make spotify playlists
    make_spotify_playlists(Session, choices, recency)






