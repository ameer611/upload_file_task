
# Upload Service API
A secure and scalable file upload service built with FastAPI, PostgreSQL, and MinIO. This service provides user authentication and allows for secure file uploads with support for various file formats.
## Features
- 🔐 User Authentication (Register/Login)
- 📤 Secure File Upload System
- 🗄️ File Storage with MinIO
- 📊 PostgreSQL Database for Metadata
- 🔍 File Format Validation
- 📝 Detailed Logging
- 🐳 Docker Containerization
## Supported File Formats
- DICOM (.dcm)
- JPEG (.jpg)
- PNG (.png)
- PDF (.pdf)
## Tech Stack
-  **FastAPI**: Modern Python web framework
-  **PostgreSQL**: Metadata and user data storage
-  **MinIO**: Object storage for files
-  **Docker**: Containerization
-  **OAuth2**: Authentication system
-  **Pydantic**: Data validation
## Getting Started
### Prerequisites
- Docker and Docker Compose
- Python 3.9 or higher (for local development)
### Installation
1. Clone the repository:
```bash
git  clone https://github.com/ameer611/upload_file_task
cd upload_file_task
```
2. Start the services using Docker Compose:
```bash
docker-compose  up  -d
```
The API will be available at `http://localhost:8000`
## API Endpoints
### Authentication
#### Register User
```http
POST /register
Content-Type: application/json
{
"username": "your_username",
"password": "your_password"
}
```
- Username must be 3-30 alphanumeric characters
- Password must be at least 8 characters
#### Login
```http
POST /token
Content-Type: application/x-www-form-urlencoded
username=your_username&password=your_password
```
Returns an access token for API authentication.
### File Upload
#### Upload File
```http
POST /upload
Authorization: Bearer <your_access_token>
Content-Type: multipart/form-data
file=@your_file
```
## Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:password@postgres:5432/db |
| MINIO_URL | MinIO server URL | minio:9000 |
| MINIO_ROOT_USER | MinIO access key | minio_user |
| MINIO_ROOT_PASSWORD | MinIO secret key | secure_password123 |
## Development
### Local Setup
1. Create a virtual environment:
```bash
python  -m  venv  venv
source  venv/bin/activate  # On Windows: venv\Scripts\activate
```
2. Install dependencies:
```bash
pip  install  -r  requirements.txt
```
3. Start the development server:
```bash
uvicorn  app.main:app  --reload
```
### Project Structure
```
.
├── app/
│ ├── main.py # Main application file
│ ├── schemas.py # Pydantic models
│ └── services/
│ ├── auth.py # Authentication service
│ ├── database.py # Database service
│ └── storage.py # Storage service
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```
## Security Features
- Password hashing
- OAuth2 authentication
- File hash verification
- Secure file storage
- Input validation
- Error logging
