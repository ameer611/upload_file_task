from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FileMetadata(Base):
    __tablename__ = "file_metadata"

    file_id = Column(String, primary_key=True)
    filename = Column(String)
    file_hash = Column(String)
    file_url = Column(String)
    file_size = Column(Integer)
    extension = Column(String)
    uploaded_by = Column(String)
    upload_date = Column(DateTime)

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    hashed_password = Column(String)