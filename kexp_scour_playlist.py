import urllib.request, json, getopt
import datetime as dt
from pytz import timezone
import pickle
import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import urllib.request, json, getopt
from bs4 import BeautifulSoup
from joint_build_database_new import band
import random
from random import shuffle
from utilities import cleanup


def KEXPharvest(show, showname, max_length):

    today = dt.date.today()
    alltracks = []

    i = 1
    while len(alltracks) < max_length and i < 20:

        showtracks = []

        offset = (today.weekday() - int(show['day'])) % 7 + (i * 7)
        showday = today - dt.timedelta(days=offset)
        showtime = show['time'] + ':00'
        combined = str(showday) + ' ' + showtime
        seattletime = dt.datetime.strptime(combined, '%Y-%m-%d %H:%M:%S')

        # This is in Pacific US timezone
        ptime = timezone('US/Pacific')
        seattletime = ptime.localize(seattletime)

        # Convert to UTC
        # friday night 2020-10-16 at 7:04 pm == 2020-10-17T02:04:10Z
        utc = timezone('UTC')
        starttime = seattletime.astimezone(utc)

        duration = show['duration']
        endtime = starttime + dt.timedelta(hours=(duration))
        startstring = dt.datetime.strftime(starttime, '%Y-%m-%dT%H:%M:%S') +'Z'
        endstring = dt.datetime.strftime(endtime, '%Y-%m-%dT%H:%M:%S') +'Z'
        url = 'https://legacy-api.kexp.org/play/?limit=200&start_time={0}&end_time={1}&ordering=-airdate'.\
            format(startstring, endstring)
        #https://legacy-api.kexp.org/play/?limit=200&start_time=2017-08-10T23:00:00&end_time=2017-08-11T02:00:00&ordering=-airdate
        print (f'{i}. {showname} playlist: \n')
        print (f'{seattletime}   -- {startstring} - {endstring}')
        #print('{3}. {2} playlist: {0} to {1}'.format(startstring, endstring, showname, i))
        print (url)
        print ('\n')
        try:

            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=hdr)
            response = urllib.request.urlopen(req)
            data = json.loads(response.read())
            dump = data['results']
            print('Success.\n')
        except getopt.GetoptError as e:
            print (str(e), '\n')
            dump = []

        #print json.dumps(data, indent=4, sort_keys=True)
        for item in dump:
            a = item['airdate']
            #2018-03-30T01:00:00Z
            b = a[:10] + ' ' + a[11:-1]
            #'2017-08-10 16:35:00'
            c = dt.datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
            c = utc.localize(c)
            s = starttime
            if c > s:
                try:
                    if item is None:
                        continue
                    if item['artist'] is None:
                        continue
                    if item['track'] is None:
                        continue
                    band = item['artist']['name']
                    song = item['track']['name']
                    try:
                        album = item['release']['name']
                    except:
                        album = ''
                    try:
                        release_year = item['releaseevent']['year']
                    except:
                        release_year = ''
                    combo = [band, song, album, release_year, showname, a[:10]]
                    print (combo)
                    showtracks.append(combo)
                except getopt.GetoptError as e:
                    pass
        alltracks = alltracks + showtracks
        print ('Tracks gathered from this show date:    {0}'.format(len(showtracks)))
        print ('Tracks gathered from this show (total): {0}\n\n'.format(len(alltracks)))
        i = i+1

    k = []
    for t1 in alltracks:
        if t1 not in k:
            k.append(t1)
    return k

def countdown():
    url = 'https://www.kexp.org/read/?category=2019-countdown'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(site, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")

    pointers = []
    morepages = True
    while morepages:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=hdr)
        page = urllib.request.urlopen(req)
        bs = BeautifulSoup(page, "html.parser")
        a = bs.find('div', {'class': 'u-grid-col u-grid-md-col9 u-md-pr3'})
        links = a.findChildren('a')
        morepages = False
        for i in links:
            x = i.text.strip()
            if x.startswith('2019 Top'):
                print (x)
                y = 'https://www.kexp.org' + i['href']
                if y not in pointers:
                    pointers.append(y) #..get_attribute('href')
                    morepages = True
        print ('\n\n')
        b = bs.findAll('a', {'class':'RoundedButton'})
        for i in b:
            if i.text.strip().startswith('View'):
                site = 'https://www.kexp.org/read/' + i['href']
                print (site)
        print ('\n\n')
        print (pointers)

    with open('2019_top_ten_links.pickle', 'wb') as handle:
        pickle.dump(pointers, handle)
    print ('Done pickling')

    return

def grablist(i):
    basesite = i
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(basesite, headers=hdr)
    page = urllib.request.urlopen(req)
    bs = BeautifulSoup(page, "html.parser")
    t = bs.find('tbody')
    s = t.findAll('tr')
    albumlist = []
    m = 0
    n = 0
    for i in s:
        x = i.text.splitlines()
        if x[1].isdigit():
            m +=1
        else:
            n +=1
    if m > n:
        a = 2
        b = 3
    else:
        a = 1
        b = 2
    for i in s:
        x = i.text.splitlines()
        artist = x[a]
        album = x[b]
        print (artist, album)
        albumlist.append([artist, album])
    return albumlist

def grab_all_lists(b):
    albumlist = []
    for i in b:
        a = grablist(i)
        for j in a:
            if j not in albumlist:
                albumlist.append(j)
    print (albumlist)
    with open('2019_top_ten_albumlist.pickle', 'wb') as handle:
        pickle.dump(albumlist, handle)


def load_to_db(albumlist):
    socket.setdefaulttimeout(15)
    # creation of the SQL database and the "session" object that is used to manage
    # communications with the database
    engine = create_engine('sqlite:///../../databases/scout.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    session = Session()

    t = dt.date.today()
    adds = 0

    for i in albumlist:
        print (i)
        clean_name = cleanup(i[0])
        n_ = band(name=i[0],
                  album=i[1],
                  source='KEXP Countdown 2019',
                  appeared ='KEXP Countdown 2019',
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

if __name__ == "__main__":
    #countdown()

    with open('2019_top_ten_links.pickle', 'rb') as handle:
        b = pickle.load(handle)
    print (b)
    grab_all_lists(b)
    with open('2019_top_ten_albumlist.pickle', 'rb') as handle:
        b = pickle.load(handle)
    print (b)
    print (len(b))
    input ('load_to_db?')
    load_to_db(b)