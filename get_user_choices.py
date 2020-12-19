# -*- coding: utf-8 -*-
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database_new import db, band


def get_user_choices(Session):
    with open('show_choices.txt', 'r') as f:
        a = f.readlines()
    print (a)
    #session = Session()
    #a = session.query(band.source).distinct()
    print ('Number of playlists to make: {0}'.format(len(a)))
    x = 0
    selections = []
    for i in a:
        x += 1
        print ('{0}. - {1}'.format(x, i.strip()))
        selections.append([str(x), i.strip()])
    print ('00. - all')
    choice = input('Enter playlists to create, each number separated by commas: \n')

    make_list = []
    if choice == '00':
        print ('Getting All')
        make_list = [i[1] for i in selections]
    else:
        y = [b.strip() for b in choice.split(',')]
        print (y)
        for j in y:
            for k in selections:
                if k[0] == j:
                    make_list.append(k[1])
    print ('Getting: {0}'.format(make_list))

    return make_list

if __name__ == '__main__':

    engine = create_engine('sqlite:///../databases/scout_new.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    #a = get_user_choices(Session)

    get_user_choices(Session)


