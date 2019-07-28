from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from geopy.geocoders import Nominatim

db = declarative_base()

class band(db):
    __tablename__ = 'band'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    song = Column(String(64))
    album = Column(String(64))
    appeared = Column(String(64), index=True)
    release_year = Column(String(64), index=True)
    comment = Column(String(64), index=True)
    source = Column(String(64), index=True)
    cleanname = Column(String(64), index=True)
    dateadded = Column(String(64), index=True)
    dateplayed = Column(String(64), index=True)
    google_nid = Column(String(64), index=True)
    google_storeID = Column(String(64), index=True)
    spotify_id = Column(String(64), index=True)
    spotify_release_date = Column(String(64), index=True)
    found_by_album = Column(Boolean, index=True)
    got_rest_of_album = Column(Boolean, index= True)

    def __repr__(self):
        return '<Table Name: %s>' % self.name
