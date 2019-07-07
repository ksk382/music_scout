from load_kexp_bands import load_kexp_bands
from load_other_bands import load_other_bands

def get_the_bands(Session, choices):


    kexp_sources = ['Swingin Doors',
                    'Roadhouse',
                    'Expansions',
                    'Street Sounds',
                    'El Toro',
                    'Jazz Theater',
                    'Sonic Reducer',
                    'Troy Nelson',
                    'Sunday Soul']

    if any(i in kexp_sources for i in choices):
        load_kexp_bands(Session, choices)

    other_sources = ['KEXP Music That Matters', 'Pitchfork Top Tracks',
                    'Stereogum', 'Metacritic', 'KCRW',
                    'Pitchfork', 'KEXP charts']

    if any(i in other_sources for i in choices):
        load_other_bands(Session, choices)


    return