from kexp_scour_playlist import KEXPharvest
import datetime as dt
import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from build_database import db, band
from utilities import shredTTOTMs, cleanup


def add_to_db(Session, k):
    session = Session()
    t = dt.date.today()
    adds = 0
    cleantracks = k
    for line in cleantracks:
        clean_name = cleanup(line[0])
        n_ = band(name=line[0],
                  song=line[1],
                  album = line[2],
                  release_year = line[3],
                  source=line[4],
                  dateplayed=line[5],
                  dateadded=t,
                  cleanname=clean_name)
        q = session.query(band).filter(band.name == n_.name, band.song == n_.song)
        if q.first() == None:
            session.add(n_)
            adds += 1
        else:
            try:
                print ('Already had {0} - {1}'.format(n_.name, n_.song))
            except:
                print ('Already had it. Cannot print. ID is {0}'.format(q.first().id))
        session.commit()
    print ('Added {0} songs'.format(adds))

    return


def load_kexp_bands(Session):

    shows = {
        'Swingin Doors': {'day': '3', 'time': '18:00', 'duration': 3},
        'Roadhouse': {'day': '2', 'time': '18:00', 'duration': 3},
        'DJ Riz': {'day': '0', 'time': '21:00', 'duration': 3},
        'Street Sounds': {'day': '6', 'time': '18:00', 'duration': 3},
        'El Toro': {'day': '2', 'time': '21:00', 'duration': 3},
        'Jazz Theater': {'day': '0', 'time': '01:00', 'duration': 2},
        'Sonic Reducer': {'day': '5', 'time': '21:00', 'duration': 3},
        'Troy Nelson': {'day': '5', 'time': '15:00', 'duration': 3}
    }

    for show in shows:
        target = shows[show]
        showname = show
        k = KEXPharvest(target, showname, max_length=800)
        add_to_db(Session, k)

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

    load_kexp_bands(Session)