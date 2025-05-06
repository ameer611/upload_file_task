from minio import Minio
from minio.error import S3Error
import io
import logging
import os

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        self.client = Minio(
            "minio:9000",
            access_key="minio_user",
            secret_key="secure_password123",
            secure=False
        )
        self.bucket_name = "uploads"
        self.external_host = os.getenv("MINIO_EXTERNAL_HOST", "localhost:9000")
        
        # Create bucket if not exists
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created MinIO bucket: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Failed to create MinIO bucket: {str(e)}")
            raise

    def upload_file(self, file_id: str, file_content: bytes, file_extension: str) -> str:
        try:
            object_name = f"{file_id}{file_extension}"
            self.client.put_object(
                self.bucket_name,
                object_name,
                io.BytesIO(file_content),
                len(file_content)
            )
            file_url = f"http://{self.external_host}/{self.bucket_name}/{object_name}"
            logger.info(f"Uploaded file to MinIO: {file_url}")
            return file_url
        except S3Error as e:
            logger.error(f"MinIO upload failed: {str(e)}")
            raise Exception(f"MinIO upload failed: {str(e)}")