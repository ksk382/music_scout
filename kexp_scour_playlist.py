import urllib.request, json, getopt
import datetime as dt
from pytz import timezone

def KEXPharvest(show, showname, max_length):

    today = dt.date.today()
    alltracks = []

    i = 0
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
        utc = timezone('UTC')
        starttime = seattletime.astimezone(utc)

        duration = show['duration']
        endtime = starttime + dt.timedelta(hours=(duration))
        startstring = dt.datetime.strftime(starttime, '%Y-%m-%dT%H:%M:%S') +'Z'
        endstring = dt.datetime.strftime(endtime, '%Y-%m-%dT%H:%M:%S') +'Z'
        url = 'https://legacy-api.kexp.org/play/?limit=200&start_time={0}&end_time={1}&ordering=-airdate'.\
            format(startstring, endstring)
        #https://legacy-api.kexp.org/play/?limit=200&start_time=2017-08-10T23:00:00&end_time=2017-08-11T02:00:00&ordering=-airdate
        print('{3}. {2} playlist: {0} to {1}'.format(startstring, endstring, showname, i))
        print (url)
        print ('\n')
        try:
            response = urllib.request.urlopen(url)
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