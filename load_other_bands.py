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
from utilities import shredTTOTMs, cleanup

bandsources = ['KEXP Music That Matters', 'Pitchfork Top Tracks',
               'Stereogum', 'Metacritic', 'KCRW',
               'Pitchfork', 'KEXP charts']

def load_other_bands(Session):
    # this loop pulls down band names from the sources identified.
    # each source, however, needs its own function, since the
    # websites are set up differently
    session = Session()
    today = dt.date.today()
    for src in bandsources:
        print(src)
        list = grabbands(src)
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
                except Exception as e:
                    print(str(e))
    cleandb(Session)
    a = shredTTOTMs(Session)
    print(('Deleted {0} TTOTM bands'.format(a)))
    return

def grabbands(src):
    maxbands = 75
    if src == 'Pitchfork':
        list = Pitchfork_charts(maxbands)
    if src == 'KEXP charts':
        maxbands = 150
        list = KEXP_charts(maxbands)
    if src == 'KCRW':
        list = KCRW_harvest(maxbands)
    if src == 'KEXP playlists':
        list = KEXP_harvest(maxbands)
    if src == 'Metacritic':
        try:
            list = metacritic(maxbands)
        except Exception as e:
            list = []
            print (str(e))
            pass
    if src == 'Stereogum':
        try:
            list = sgum(maxbands)
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









