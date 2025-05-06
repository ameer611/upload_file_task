from pydantic import BaseModel

class FileResponse(BaseModel):
    file_id: str
    file_url: str
    filename: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str