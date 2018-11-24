from showtime_get_bands import Pitchfork_charts, KCRW_harvest, \
    KEXP_charts, KEXP_harvest, metacritic, sgum, pfork_tracks, \
    MTM
from utilities import cleandb, cleanup, shredTTOTMs
import datetime as dt
import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from build_database import db, band
from send_it import send_it, get_ids


def make_playlists(Session):
    session = Session()
    a = session.query(band.source).distinct()
    print ('Number of playlists to make: {0}'.format(a.count()))
    for i in a:
        playlist_name = i[0]
        print (playlist_name)
        tracks = session.query(band).filter(band.source==playlist_name)
        print ('{0} tracks found for {1}'.format(tracks.count(), playlist_name))
        print (get_ids(Session, playlist_name))
        print (send_it(Session, playlist_name, recency=2018))
    return


if __name__ == "__main__":

    socket.setdefaulttimeout(10)
    # creation of the SQL database and the "session" object that is used to manage
    # communications with the database
    engine = create_engine('sqlite:///../databases/scout.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    print ('Making playlists')
    make_playlists(Session)
    print ('Done making playlists')