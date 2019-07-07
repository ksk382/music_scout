import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from build_database import db, band
from send_it import send_it, send_it_top90, get_ids
from sqlalchemy.sql.expression import func

def make_playlists(Session, choices, recency):
    session = Session()
    for i in choices:
        playlist_name = i
        print (playlist_name)
        tracks = session.query(band).filter(band.source == playlist_name)
        print ('{0} tracks found for {1}'.format(tracks.count(), playlist_name))
        print (get_ids(Session, playlist_name))
        try:
            send_it(Session, playlist_name, recency=recency)
        except Exception as e:
            print (str(e))
            print ('Playlist failed: {0}'.format(playlist_name))
    return

def top_90(Session):
    session = Session()
    playlist_name = 'Scout Top 90'
    print (playlist_name)
    tracks = session.query(band).filter(band.appeared == playlist_name)
    print ('{0} tracks found for {1}'.format(tracks.count(), playlist_name))
    print (get_ids(Session, playlist_name))
    send_it_top90(Session, playlist_name, recency=2018)

if __name__ == "__main__":

    socket.setdefaulttimeout(10)
    # creation of the SQL database and the "session" object that is used to manage
    # communications with the database
    engine = create_engine('sqlite:///'sqlite:///../../databases/scout.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    print ('Making playlists')
    make_playlists(Session)
    print ('Done making playlists')