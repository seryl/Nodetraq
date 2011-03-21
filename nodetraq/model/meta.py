"""SQLAlchemy Metadata and Session object"""
import datetime
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['Session', 'metadata', 'Base', 'now']

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database
metadata = MetaData()

# declarative table definitions
Base = declarative_base()

def now():
    return datetime.datetime.now()
