import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from models import Base

database_name = "espnFFdata"

try:
    db_url = f"sqlite:///{database_name}"
    engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine)
except OperationalError as err:
    logging.error("Cannot connect to DB %s", err)
    raise err


Session = sessionmaker(bind=engine)
session = Session()
