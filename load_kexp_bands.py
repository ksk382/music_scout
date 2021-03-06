from kexp_scour_playlist import KEXPharvest
import datetime as dt
import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database_new import db, band
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
                  appeared=line[4],
                  dateplayed=line[5],
                  dateadded=t,
                  cleanname=clean_name)
        q = session.query(band).filter(band.name == n_.name, band.song == n_.song, band.source == n_.source)
        if q.first() == None:
            session.add(n_)
            adds += 1
        else:
            try:
                print ('Already had {0} - {1}'.format(n_.name, n_.song))
            except:
                print ('Already had it. Cannot print. ID is {0}'.format(q.first().id))
        session.commit()

    return adds


def load_kexp_bands(Session, choices):

    # times are in PST
    # friday night 2020-10-16 at 7:04 pm == 2020-10-17T02:04:10Z
    shows = {
        'Swingin Doors': {'day': '3', 'time': '18:00', 'duration': 3},
        'Roadhouse': {'day': '2', 'time': '18:00', 'duration': 3},
        'Expansions': {'day': '6', 'time': '21:00', 'duration': 3},
        'Street Sounds': {'day': '4', 'time': '21:00', 'duration': 3},
        'El Toro': {'day': '2', 'time': '21:00', 'duration': 3},
        'Jazz Theater': {'day': '0', 'time': '03:00', 'duration': 2},
        'Sonic Reducer': {'day': '5', 'time': '21:00', 'duration': 3},
        'Troy Nelson': {'day': '5', 'time': '15:00', 'duration': 3},
        'Sunday Soul': {'day': '6', 'time': '18:00', 'duration': 3},
        'Friday Night': {'day': '4', 'time': '19:00', 'duration': 3},
        'Pacific Notions': {'day': '6', 'time': '06:00', 'duration': 3}
    }


    for show in shows:
        if show in choices:
            target = shows[show]
            showname = show
            try:
                k = KEXPharvest(target, showname, max_length=800)
                count = add_to_db(Session, k)
                print ('Added {0} songs to {1}'.format(count, showname))
            except Exception as e:
                print ('Failed collecting {0} \n {1}'.format(showname, str(e)))

    if 'Morning Show' in choices:
        showname = 'Morning Show'
        for weekday in range(0,5):
            try:
                target = {'day': str(weekday), 'time': '06:00', 'duration': 3}
                k = KEXPharvest(target, showname, max_length=800)
                count = add_to_db(Session, k)
                print ('Added {0} songs to {1}'.format(count, showname))
            except Exception as e:
                print ('Failed collecting {0} \n {1}'.format(showname, str(e)))

    print ('Done with load_kexp_bands\n\n')
    return


if __name__ == "__main__":

    socket.setdefaulttimeout(10)
    # creation of the SQL database and the "session" object that is used to manage
    # communications with the database
    engine = create_engine('sqlite:///../../databases/scout.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    load_kexp_bands(Session, ['Sunday Soul', 'Expansions', 'Street Sounds'])