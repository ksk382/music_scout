import socket
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from build_database import db, band


if __name__ == "__main__":

    socket.setdefaulttimeout(10)
    # creation of the SQL database and the "session" object that is used to manage
    # communications with the database
    engine = create_engine('sqlite:///../databases/scout.db')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    metadata = MetaData(db)
    db.metadata.create_all(engine)

    session = Session()

    a = session.query(band)

