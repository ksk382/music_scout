# -*- coding: utf-8 -*-
import datetime as dt
import socket
import sys
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database_new import db, band
from joint_spotify_work import find_spotify_ids, \
    find_spotify_ids_choices, get_spotify_ids, fill_in_release_dates
from get_user_choices import get_user_choices, get_all_shows
from get_the_bands import get_the_bands
from make_spotify_playlists import make_spotify_playlists
from sqlalchemy import or_
from utilities import cleandb
import datetime as dt
from dateutil.relativedelta import relativedelta
from get_album_tracks import get_album_tracks
import argparse

def clear_failed_2s(Session):

    session = Session()
    a = session.query(band).filter(band.spotify_id=='failed 2')
    print (a.count())
    for i in a:
        i.spotify_id = None
    session.commit()
    input('cleared all the failed 2s')


if __name__ == '__main__':
    engine = create_engine('sqlite:///../databases/scout_new.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-a', '--all',
                        help='Enter -a yes',
                        required=False)
    args = vars(parser.parse_args())

    if args['all'] != None:
        choices = get_all_shows(Session)
        recency = '1900'
        remove_TTOTM_tracks = False

    else:
        choices = get_user_choices(Session)
        recency = input('\n\nEnter oldest year to include: \n')
        ttotm_selection = input('\n\nExclude bands used by TTOTM? (y/n): \n')
        if ttotm_selection == 'y':
            remove_TTOTM_tracks = True
        else:
            remove_TTOTM_tracks = False

    #clear_failed_2s(Session)

    # get user input--which shows to make playlists for


    # find some bands
    get_the_bands(Session, choices)

    # insert album tracks for album listings
    get_album_tracks(Session)

    # get the spotify IDs for them
    get_spotify_ids(Session, choices)

    # make spotify playlists
    cleandb(Session, remove_TTOTM_tracks)
    fill_in_release_dates(Session)
    errors = make_spotify_playlists(Session, choices, recency)
    for i in errors:
        print (i)






