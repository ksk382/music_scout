from showtime_get_bands import Pitchfork_charts, KCRW_harvest, \
    KEXP_charts, metacritic, sgum, pfork_tracks, \
    MTM
from utilities import cleandb, cleanup, shredTTOTMs
import datetime as dt
import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from build_database import db, band
from utilities import shredTTOTMs, cleanup

bandsources = ['KEXP Music That Matters', 'Pitchfork Top Tracks',
               'Stereogum', 'Metacritic', 'KCRW',
               'Pitchfork', 'KEXP charts']

def load_other_bands(Session, choices):
    # this loop pulls down band names from the sources identified.
    # each source, however, needs its own function, since the
    # websites are set up differently

    proceed = False
    for src in choices:
        if src in bandsources:
            # at least one of the choices needs to be in bandsources
            # or else this function doesn't need to proceed
            proceed = True
    if proceed == False:
        return
    session = Session()
    today = dt.date.today()
    for src in choices:
        print('\n\n\n', src)
        try:
            list = grabbands(src)
        except Exception as e:
            print ('{0} not provided for in load_other_bands.grabbands'.format(src))
            print (str(e))
        add_count = 0
        for i in list:
            h = cleanup(i.name)
            if h != '':
                try:
                    q = session.query(band).filter(band.cleanname == h)
                    if q.first() == None:
                        i.source = src
                        i.cleanname = h
                        i.dateadded = today
                        #newband = i(name=i, source=src, cleanname=h, dateadded=today)
                        print("Adding {0} (from {1})".format(i.name, i.source))
                        session.add(i)
                        session.commit()
                        add_count+=1
                except Exception as e:
                    print(str(e))
        print ('Added {0} entries to the {1} collection. \n\n'.format(add_count, src))
    cleandb(Session)
    return

def grabbands(src):
    if src == 'Pitchfork':
        list = Pitchfork_charts(25)
    if src == 'KEXP charts':
        list = KEXP_charts(150)
    if src == 'KCRW':
        list = KCRW_harvest(200)
    if src == 'Metacritic':
        try:
            list = metacritic(75)
        except Exception as e:
            list = []
            print (str(e))
            pass
    if src == 'Stereogum':
        try:
            list = sgum(25)
        except Exception as e:
            list = []
            print (str(e))
            pass
    if src == 'Pitchfork Top Tracks':
        try:
            list = pfork_tracks(200)
        except Exception as e:
            list = []
            print (str(e))
            pass
    if src == 'KEXP Music That Matters':
        try:
            list = MTM(200)
        except Exception as e:
            list = []
            print (str(e))
            pass
    return list

if __name__ == "__main__":

    socket.setdefaulttimeout(10)
    # creation of the SQL database and the "session" object that is used to manage
    # communications with the database
    engine = create_engine('sqlite:///../databases/scout.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    print ('Getting bands')
    load_other_bands(Session)
    print ('Done getting bands')









