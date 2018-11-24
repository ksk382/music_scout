import os


def get_creds():

    cwd = os.getcwd()
    dirlist = os.listdir(cwd)
    foundpath = False
    for i in dirlist:
        if 'client_secret_' in i:
            with open(i, 'r') as f:
                client_secret_pathname = f.readline().rstrip()
            foundpath = True

    if foundpath:
        i = 'gmusic_creds'
        fname = client_secret_pathname + i
        with open(fname) as f:
            content = f.readlines()
    else:
        print('Failed to find pathname')

    return content

print (get_creds())