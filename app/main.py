from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from .schemas import FileResponse, UserCreate, UserResponse, Token
from .services.storage import StorageService
from .services.database import DatabaseService
from .services.auth import AuthService
from .dependencies import get_current_user
import hashlib
import uuid
from datetime import datetime
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Upload Service API")

ALLOWED_EXTENSIONS = {'.dcm', '.jpg', '.png', '.pdf'}

class User(BaseModel):
    username: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    db_service = DatabaseService()
    auth_service = AuthService()
    
    try:
        # Validate username (alphanumeric, 3-30 characters)
        if not re.match(r"^[a-zA-Z0-9]{3,30}$", user.username):
            logger.error(f"Registration failed: Invalid username {user.username}")
            raise HTTPException(status_code=400, detail="Username must be 3-30 alphanumeric characters")
        
        # Check if user already exists
        if db_service.get_user_by_username(user.username):
            logger.error(f"Registration failed: Username {user.username} already exists")
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Validate password length
        if len(user.password) < 8:
            logger.error(f"Registration failed: Password too short for {user.username}")
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
        
        # Hash password and create user
        hashed_password = auth_service.get_password_hash(user.password)
        user_data = {
            "username": user.username,
            "hashed_password": hashed_password
        }
        db_service.create_user(user_data)
        logger.info(f"User {user.username} registered successfully")
        
        return UserResponse(username=user.username)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db_service = DatabaseService()
    auth_service = AuthService()
    
    try:
        db_user = db_service.get_user_by_username(form_data.username)
        if not db_user:
            logger.error(f"Login failed: Username {form_data.username} not found")
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        if not auth_service.verify_password(form_data.password, db_user.hashed_password):
            logger.error(f"Login failed: Incorrect password for {form_data.username}")
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        access_token = auth_service.create_access_token(data={"sub": form_data.username})
        logger.info(f"User {form_data.username} logged in successfully")
        return Token(access_token=access_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Validate file extension
    file_extension = f".{file.filename.split('.')[-1].lower()}"
    if file_extension not in ALLOWED_EXTENSIONS:
        logger.error(f"Upload failed: Unsupported file format {file_extension}")
        raise HTTPException(status_code=400, detail="Unsupported file format")

    # Generate file ID and hash
    file_id = str(uuid.uuid4())
    file_content = await file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()

    # Initialize services
    storage_service = StorageService()
    db_service = DatabaseService()

    try:
        # Upload to MinIO
        file_url = storage_service.upload_file(
            file_id=file_id,
            file_content=file_content,
            file_extension=file_extension
        )

        # Save metadata to PostgreSQL
        metadata = {
            "file_id": file_id,
            "filename": file.filename,
            "file_hash": file_hash,
            "file_url": file_url,
            "file_size": len(file_content),
            "extension": file_extension,
            "uploaded_by": current_user.username,
            "upload_date": datetime.utcnow()
        }
        db_service.save_metadata(metadata)
        logger.info(f"File {file.filename} uploaded successfully by {current_user.username}")

        return FileResponse(
            file_id=file_id,
            file_url=file_url,
            filename=file.filename
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))