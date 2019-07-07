# -*- coding: utf-8 -*-
import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from joint_build_database_old import db as db1, band as band1
from joint_build_database_new import db as db2, band as band2
import pandas as pd


socket.setdefaulttimeout(10)
# creation of the SQL database and the "session" object that is used to manage
# communications with the database
engine = create_engine('sqlite:///../../databases/scout_new.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
metadata = MetaData(db1)
db1.metadata.create_all(engine)
sess1 = Session()

engine = create_engine('sqlite:///../../databases/scout_new_new.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
metadata = MetaData(db2)
db2.metadata.create_all(engine)
sess2 = Session()


df1 = pd.read_sql(sess1.query(band1).statement, sess1.bind)

df2 = df1
df2['spotify_release_date'] = df1['spotify_release_year']

print (df2.columns)
df2 = df2[[]]
print (df2.columns)
input('enter to sql?')

df2.to_sql('band', con=engine, index = False, if_exists='replace')
sess2.commit()





