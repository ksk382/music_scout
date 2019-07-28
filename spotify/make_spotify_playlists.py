from joint_build_database_new import band
from joint_spotify_work import do_a_playlist, fill_in_release_dates, splog_on

def make_spotify_playlists(Session, choices, recency):
    session = Session()
    for i in choices:
        a = session.query(band).filter(band.source==i).filter(band.spotify_id != None).filter(band.spotify_release_date != None)
        b = []
        a = [x for x in a if len(x.spotify_id) == 22]  # check proper spotify id, length ==22
        for j in a:
            try:
                if int(j.spotify_release_date[:4]) >= int(recency):
                    b.append(j)
                else:
                    print ('no go: ', j.spotify_release_date)
            except:
                print ('no go error: ', j.spotify_release_date)
        print ('Creating {} playlist. {} tracks found'.format(i, len(b)))
        ids_to_add = [c.spotify_id for c in a]
        ids_to_add = [x for x in ids_to_add if len(x) == 22]
        playlist_name = 'Scout ' + i
        do_a_playlist(ids_to_add, playlist_name)

    return