from joint_build_database_new import db, band


def get_user_choices(Session):
    session = Session()
    a = session.query(band.source).distinct()
    print ('Number of playlists to make: {0}'.format(a.count()))
    x = 0
    selections = []
    for i in a:
        x += 1
        print ('{0}. - {1}'.format(x, i[0]))
        selections.append([str(x), i[0]])
    print ('00. - all')
    choice = input('Enter playlists to create, each number separated by commas: \n')

    if choice == '00':
        print ('Getting All')
        a = session.query(band.source).distinct()
        b = []
        for i in a:
            b.append(i[0])
        a = b
    else:
        y = [b.strip() for b in choice.split(',')]
        print (y)
        a = []
        for j in y:
            for k in selections:
                if k[0] == j:
                    a.append(k[1])
    print ('Getting: {0}'.format(a))

    return a