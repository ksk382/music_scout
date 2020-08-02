# -*- coding: utf-8 -*-
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database_new import db, band
from joint_spotify_work import splog_on
import pprint


def get_album_tracks(Session):
    session = Session()
    a = session.query(band).filter(band.album != '').filter(band.song == None, band.got_rest_of_album == None)
    sp, username = splog_on()
    pp = pprint.PrettyPrinter(indent=4)

    for i in a:
        artist = i.name
        album = i.album
        i.found_by_album = True
        print (f'{artist} - {album} - {i.got_rest_of_album}')

        query1 = 'artist:{0} album:{1}'.format(artist, album)
        results = sp.search(q=query1, type='track')
        try:
            d = results['tracks']['items'][0]['album']
        except:
            continue
        uri = d['uri']
        e = sp.album_tracks(uri)
        f = e['items']
        for j in f:
            new_track = band(name=artist,
                             song=j['name'],
                             appeared=i.appeared,
                             source=i.source,
                             album=i.album,
                             cleanname=i.cleanname,
                             dateadded=i.dateadded,
                             spotify_id=j['id'],
                             spotify_release_date=d['release_date'],
                             found_by_album=True
                             )
            print (f'{new_track.name}, {new_track.song}')
            session.add(new_track)
        i.got_rest_of_album = True
        session.commit()


if __name__ == '__main__':

    engine = create_engine('sqlite:///../databases/scout_new.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    #a = get_user_choices(Session)
    get_album_tracks(Session)
