from joint_build_database_new import band
from joint_spotify_work import do_a_playlist

def make_spotify_playlists(Session, choices, recency):
    session = Session()
    for i in choices:
        a = session.query(band).filter(band.source==i).filter(band.spotify_id != None)
        print ('Creating {} playlist. {} tracks found'.format(i, a.count()))
        for b in a:
            print (b.spotify_id)
        ids_to_add = [b.spotify_id for b in a]
        ids_to_add = [x for x in ids_to_add if len(x) == 22] #check proper spotify id, length ==22
        ids_to_add = [x for x in ids_to_add if int(x.spotify_release_date[:4]) >= recency]
        playlist_name = 'Scout ' + i
        do_a_playlist(ids_to_add, playlist_name)

    return