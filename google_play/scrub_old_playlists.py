from send_it import get_creds
from gmusicapi import Mobileclient
from pprint import pprint
import pickle

content = get_creds()

api = Mobileclient()
api.login(content[0], content[1], Mobileclient.FROM_MAC_ADDRESS)

allcontents = api.get_all_user_playlist_contents()
y = []
x = 1
for i in allcontents:
    y.append([x, i['id'], i['name']])
    x += 1
    if i['name'] == 'May 29, 2018 Dinner Party':
        pprint (i)
        x = i['tracks']

a = []
for j in x:
    y = [j['track']['artist'], j['track']['title']]
    a.append(y)

print (a)

with open('../track_dump.pickle', 'wb') as f:
    pickle.dump(a, f)

choice = 1

'''
while str(choice) != '0':
    x = 1
    for i in y:
        i[0] = x
        print ('{0}. {1}'.format(x, i[2]))
        x += 1
    print ('{0}. {1}'.format(0, 'quit'))
    choice = input('make choice\n')
    print ('\n', y)
    print (choice)
    for j in y:
        if str(j[0]) == str(choice):
            print (j)
            playlist_id = j[1]
            api.delete_playlist(playlist_id)
            y.remove(j)
'''