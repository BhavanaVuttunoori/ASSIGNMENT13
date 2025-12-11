JWT Authentication API - Assignment 13
The Assignment 13 deliverable is a fully tested FastAPI authentication service with JWT implementation, packaged for local development, Docker usage, and CI/CD. This README documents how the project is structured, what was implemented, and how to reproduce the results.

Project Highlights
Built with FastAPI and SQLAlchemy to expose authentication endpoints through REST API with database persistence. JWT token-based authentication with secure password hashing using bcrypt. Robust Pydantic validation in schemas.py with explicit error handling (email format, password strength, duplicate users). Comprehensive automated test suite with Playwright E2E tests covering positive and negative scenarios (11 tests). SQLAlchemy ORM models with User table including email, username, and hashed password storage. Continuous Integration via GitHub Actions to test with PostgreSQL, build Docker images, and deploy to Docker Hub. Containerized delivery: public Docker image available at bhavanavuttunoori/jwt-auth-api. Front-end HTML pages with client-side validation for registration and login.

Getting Started
1. Setup Environment
cd "assign 13 web api"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
2. Run the Application Locally
python main.py
Navigate to http://localhost:8000/docs for the Swagger UI or access front-end pages at http://localhost:8000/static/register.html and http://localhost:8000/static/login.html.

Docker Usage
Build Locally (optional)
docker build -t jwt-auth-api .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:password@host:5432/authdb -e SECRET_KEY=your-secret-key jwt-auth-api
Pull Prebuilt Image
docker pull bhavanavuttunoori/jwt-auth-api:latest
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:password@host:5432/authdb -e SECRET_KEY=your-secret-key bhavanavuttunoori/jwt-auth-api:latest
Using Docker Compose
docker-compose up -d
The application will be available at http://localhost:8000 with PostgreSQL database.

Testing Strategy
E2E Tests (tests/test_auth.py): Playwright tests covering user registration and login flows. Positive Tests: Valid registration, successful login with correct credentials, UI elements verification. Negative Tests: Short password, password without numbers, mismatched passwords, invalid email format, wrong password login, non-existent user, duplicate email, short username.

Run the full suite:

pytest tests/test_auth.py -v
Run specific test:

pytest tests/test_auth.py::test_register_with_valid_data -v
Project Structure
assign 13 web api/
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions CI/CD pipeline
├── static/
│   ├── register.html        # Registration page with client-side validation
│   └── login.html           # Login page with JWT token display
├── tests/
│   ├── conftest.py          # Pytest configuration and fixtures
│   └── test_auth.py         # Playwright E2E tests (11 tests)
├── auth.py                  # JWT token generation and password hashing utilities
├── database.py              # Database configuration and User model
├── main.py                  # FastAPI application with authentication endpoints
├── schemas.py               # Pydantic validation schemas
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Multi-container orchestration
├── pytest.ini               # Pytest configuration
├── .env.example             # Environment variables template
└── README.md                # This file
API Endpoints
Authentication Operations
Register User:

POST /register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123"
}
Response (201):

{
  "message": "User registered successfully",
  "detail": "User johndoe has been created"
}
Login User:

POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
Response (200):

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
Get Current User (Protected):

GET /users/me?token=<jwt_token>
Response (200):

{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2025-12-10T10:00:00"
}
Health Check:

GET /health
Response (200):

{
  "status": "healthy"
}
Pydantic Validation Implementation
The Pydantic schemas in schemas.py provide comprehensive validation:

UserCreate Schema:

Email validation using EmailStr type for proper email format. Username validation: 3-50 characters, alphanumeric with underscores/hyphens allowed. Password validation: Minimum 8 characters, must contain at least one letter and one digit. Custom validators enforce password strength requirements.

UserLogin Schema:

Email and password fields with EmailStr validation.

Token Schema:

access_token field for JWT token. token_type field defaulting to "bearer".

MessageResponse Schema:

Generic response schema for success/error messages.

Example validation in schemas.py:

from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v
JWT Authentication Implementation
The JWT authentication in auth.py uses python-jose and passlib:

Password Hashing:

Uses bcrypt algorithm via passlib for secure password hashing. Automatic salt generation for each password. verify_password() function to check plain password against hashed password.

JWT Token Generation:

create_access_token() function creates signed JWT tokens. Tokens include user email and username in payload. Configurable expiration time (default 30 minutes). Uses HS256 algorithm with secret key.

Token Verification:

verify_token() function decodes and validates JWT tokens. Returns user email from token payload if valid. Returns None for invalid or expired tokens.

Database Schema
Users Table:

id (Integer, Primary Key, Auto-increment)
email (String, Unique, Indexed)
username (String, Unique, Indexed)
hashed_password (String)
created_at (DateTime, Auto-set on creation)
Front-End Implementation
Registration Page (static/register.html)
Features:

Email input with HTML5 and JavaScript validation. Username input with length validation (3-50 characters). Password input with real-time strength indicator showing: At least 8 characters requirement. Contains letter requirement. Contains number requirement. Confirm password field with matching validation. Client-side validation before form submission. Success message display on successful registration. Error message display for validation failures or server errors. Responsive design with gradient background. Loading spinner during API calls.

Validation Flow:

User types in form fields. Real-time validation provides immediate feedback. Password requirements turn green as conditions are met. On submit, client-side validation runs first. If valid, POST request sent to /register endpoint. Server validates with Pydantic schemas. Success or error message displayed based on response.

Login Page (static/login.html)
Features:

Email input with format validation. Password input. Client-side validation before submission. JWT token display section (for demonstration). Token automatically stored in localStorage. Success message on successful login. Error message for invalid credentials (401). Responsive design matching registration page. Loading spinner during API calls.

Authentication Flow:

User enters email and password. Client validates input format. POST request sent to /login endpoint. Server verifies credentials and password hash. On success, JWT token returned and displayed. Token stored in localStorage for future requests. On failure, error message shown.

Continuous Integration
The repository includes a GitHub Actions workflow (.github/workflows/ci-cd.yml) that runs on every push to main/master:

Test Job:

Set up Python 3.11 environment. Start PostgreSQL 15 service container with health checks. Install dependencies including Playwright. Install Playwright Chromium browser. Set environment variables (DATABASE_URL, SECRET_KEY). Initialize database tables. Start FastAPI server in background. Wait for server to be ready with health check polling. Run Playwright E2E tests with pytest. Upload test results and reports as artifacts.

Build and Push Job (main/master branch only):

Set up Docker Buildx for multi-platform builds. Log in to Docker Hub using secrets. Extract metadata for image tagging. Build Docker image with optimizations. Tag with 'latest' and commit SHA. Push to Docker Hub repository. Implement build caching for faster builds.

Required GitHub Secrets
DOCKER_USERNAME: Your Docker Hub username DOCKER_PASSWORD: Your Docker Hub access token or password

Assignment Instructions & Deliverables
Objective: Implement JWT-based authentication with user registration and login, front-end pages, Playwright E2E tests, and maintain CI/CD pipeline for automated testing and deployment.

Implementation Checklist
JWT authentication with /register and /login endpoints. Password hashing with bcrypt for secure storage. Pydantic validation with custom validators for email, username, and password. Front-end registration page with client-side validation. Front-end login page with JWT token storage. Playwright E2E tests covering positive scenarios (valid registration, successful login). Playwright E2E tests covering negative scenarios (short password, invalid email, wrong credentials, duplicates). GitHub Actions workflow with PostgreSQL integration. Automated Playwright test execution in CI. Docker containerization with docker-compose support. Automated Docker Hub deployment on successful tests. Comprehensive documentation.

Submission Package
GitHub repository: https://github.com/BhavanaVuttunoori/ASSIGNMENT13 Docker Hub image: bhavanavuttunoori/jwt-auth-api Screenshots demonstrating:

Successful GitHub Actions workflow with all tests passing
Playwright E2E tests passing locally
Registration page functioning with validation
Login page functioning with JWT token display
Grading Guidelines
Criterion: JWT Authentication

/register endpoint with duplicate checking, password hashing, and database storage
/login endpoint returning JWT on valid credentials, 401 on invalid
Pydantic validation for user input
Criterion: Front-End Pages

register.html with email, password fields and client-side validation
login.html with email, password fields and success token display
Client-side checks for email format and password requirements
Criterion: Playwright E2E Tests

Positive tests: valid registration, successful login
Negative tests: short password, invalid inputs, wrong credentials
Tests verify UI states and server responses
Proper use of locators and assertions
Criterion: CI/CD Pipeline

GitHub Actions workflow configured
PostgreSQL service container for testing
Playwright tests run automatically
Docker image built and pushed on success
Criterion: Documentation

README with setup, running, and testing instructions
Docker Hub repository link
Code comments and docstrings
Helpful Commands
Task	Command
Install dependencies	pip install -r requirements.txt
Install Playwright	playwright install chromium
Run application	python main.py
Run application with uvicorn	uvicorn main:app --reload
Run all E2E tests	pytest tests/test_auth.py -v
Run specific test	pytest tests/test_auth.py::test_register_with_valid_data -v
Build Docker image	docker build -t jwt-auth-api .
Run with Docker Compose	docker-compose up -d
Stop Docker Compose	docker-compose down
View container logs	docker-compose logs -f api
Access registration page	http://localhost:8000/static/register.html
Access login page	http://localhost:8000/static/login.html
Access API docs	http://localhost:8000/docs
Submission Tips
Ensure all 11 Playwright tests pass locally before pushing. Verify GitHub Actions workflow completes successfully with green checkmarks. Confirm Docker image is pushed to Docker Hub and publicly accessible. Capture screenshots of GitHub Actions success, tests passing, and front-end pages. Test Docker image by pulling and running it locally. Include Docker Hub link in README. Keep SECRET_KEY and sensitive data in environment variables, not in code. Use .gitignore to exclude .env files from version control.

Learning Outcomes
CLO3: Create Python applications with automated testing

Playwright E2E tests for registration and login flows
Test fixtures and browser automation
Positive and negative test scenarios
11 comprehensive tests covering edge cases
CLO4: Set up GitHub Actions for CI

Automated testing on every push
PostgreSQL service containers in CI
Automated Docker builds on successful tests
Docker Hub deployment automation
CLO9: Apply containerization techniques

Dockerfile for FastAPI application
Docker Compose for multi-container setup
Environment variable management
PostgreSQL container integration
CLO10: Create, consume, and test REST APIs

FastAPI REST endpoints for authentication
JSON request/response handling
Status code management (200, 201, 400, 401)
API documentation with Swagger
CLO11: Integrate with SQL databases

SQLAlchemy ORM for database operations
User model with unique constraints
Database session management
PostgreSQL for production, initialization on startup
CLO12: Serialize/deserialize JSON with Pydantic

Input validation with Pydantic schemas
Custom validators for business logic
Type safety with EmailStr and Field
Automatic error responses for validation failures
CLO13: Secure authentication and authorization

JWT token generation and verification
Bcrypt password hashing with automatic salting
Secure password storage (never plain text)
Token-based authentication flow
Password strength requirements enforcement
Author
Bhavana Vuttunoori GitHub: https://github.com/BhavanaVuttunoori Repository: https://github.com/BhavanaVuttunoori/ASSIGNMENT13

Acknowledgments
FastAPI documentation and JWT authentication examples. SQLAlchemy ORM patterns and best practices. Playwright E2E testing framework and documentation. Pydantic validation framework. GitHub Actions workflow templates. Course instructors for project requirements and guidance.

Support
For questions or issues:

Review the API documentation at http://localhost:8000/docs
Check test outputs for detailed error messages
Verify environment variables are set correctly
Ensure PostgreSQL is running and accessible
Check GitHub Actions logs for CI/CD issues
License
This project is for educational purposes as part of Assignment 13 for demonstrating JWT authentication, front-end integration, E2E testing, and CI/CD pipelines.

Note: This project was created as part of Assignment 13 for demonstrating JWT-based authentication with user registration and login, responsive front-end pages, comprehensive Playwright E2E testing, and automated CI/CD deployment.

About
JWT Authentication API with FastAPI, PostgreSQL, Playwright E2E tests, and CI/CD pipeline for Assignment 13.
#   T r i g g e r   w o r k f l o w  
 