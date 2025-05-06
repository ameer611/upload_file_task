from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base, FileMetadata, User
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.engine = create_engine("postgresql://user:password@postgres:5432/db")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("Database connection initialized")

    def save_metadata(self, metadata: dict):
        session = self.Session()
        try:
            file_metadata = FileMetadata(
                file_id=metadata["file_id"],
                filename=metadata["filename"],
                file_hash=metadata["file_hash"],
                file_url=metadata["file_url"],
                file_size=metadata["file_size"],
                extension=metadata["extension"],
                uploaded_by=metadata["uploaded_by"],
                upload_date=metadata["upload_date"]
            )
            session.add(file_metadata)
            session.commit()
            logger.info(f"Saved metadata for file: {metadata['file_id']}")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save metadata: {str(e)}")
            raise e
        finally:
            session.close()

    def create_user(self, user_data: dict):
        session = self.Session()
        try:
            user = User(
                username=user_data["username"],
                hashed_password=user_data["hashed_password"]
            )
            session.add(user)
            session.commit()
            logger.info(f"Created user: {user_data['username']}")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create user: {str(e)}")
            raise e
        finally:
            session.close()

    def get_user_by_username(self, username: str):
        session = self.Session()
        try:
            user = session.query(User).filter(User.username == username).first()
            logger.info(f"Retrieved user: {username}")
            return user
        except Exception as e:
            logger.error(f"Failed to retrieve user {username}: {str(e)}")
            raise e
        finally:
            session.close()