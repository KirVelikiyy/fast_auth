# Microservice Authorization and Registration with FastAPI
## Overview
This repository contains a microservice for user authentication and registration built using FastAPI in Python. The application leverages Docker Compose for containerization. To get started, clone this repository and follow the setup instructions below.

## Prerequisites
- Docker  
- Docker Compose

## Stack

**Server:** FastAPI, uvicorn  
**Database:** PostgreSQL  
**ORM:** SQLAlchemy, Alembic  
**Encryption:** PyJWT

## Setup
### Clone the repository:

```bash
git clone https://github.com/KirVelikiyy/fast_auth.git
cd fast_auth
```
Create a .env file in the project root and configure the following variables:

```
SECRET_KEY=mysecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_HOURS=24

POSTGRES_DB=your_database
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=postgres_pass
POSTGRES_PORT=5432
POSTGRES_HOST_AUTH_METHOD=md5

# postgresql://[ user:pass @][ hostspec ][/ dbname ]
POSTGRES_URI=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres/${POSTGRES_DB}
DEV_POSTGRES_URI=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost/${POSTGRES_DB}
```
Adjust the values according to your security preferences.

Build and run the containers using Docker Compose:

```bash
docker-compose up -d --build
```
Visit http://localhost:8000/docs in your browser to access the FastAPI Swagger documentation.

# JWT Token System
The authentication system is based on JSON Web Tokens (JWT), consisting of access and refresh tokens. Token rotation is implemented to enhance security by regularly refreshing the refresh tokens.

# Endpoints
GET /docs: OpenAPI swagger API documentation.

POST /register: Register a new user.

POST /login: Obtain an access token and a refresh token by providing valid credentials.

POST /refresh: Refresh the access token using a valid refresh token.

GET /users/me: Get information about the current user.
