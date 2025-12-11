# JWT Authentication API - Assignment 13

The Assignment 13 deliverable is a fully tested FastAPI JWT authentication service with user registration and login, packaged for local development, Docker usage, and CI/CD. This README documents how the project is structured, what was implemented, and how to reproduce the results.

## Project Highlights

Built with FastAPI and SQLAlchemy to expose user registration and login endpoints with JWT token-based authentication and database persistence. Secure user authentication with bcrypt password hashing and JWT token generation. Front-end HTML pages with client-side validation for registration and login. Robust Pydantic validation in schemas.py with explicit error handling (email format, password strength, username validation). Comprehensive automated Playwright E2E test suite covering authentication scenarios. SQLAlchemy ORM User model with proper password hashing. Continuous Integration via GitHub Actions to test with PostgreSQL and Playwright. Containerized delivery: Docker image ready for deployment at bhavanavuttunoori/jwt-auth-api.

## Getting Started

### 1. Setup Environment

```powershell
cd "assign 13 web api"
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Run the Application Locally

```powershell
uvicorn main:app --reload
```

Navigate to http://localhost:8000/static/register.html for registration or http://localhost:8000/static/login.html for login.

## Docker Usage

### Build Locally (optional)

```bash
docker build -t jwt-auth-api .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:password@localhost:5432/authdb jwt-auth-api
```

### Pull Prebuilt Image

```bash
docker pull bhavanavuttunoori/jwt-auth-api:latest
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:password@localhost:5432/authdb bhavanavuttunoori/jwt-auth-api:latest
```

### Using Docker Compose

```bash
docker-compose up -d
```

The application will be available at http://localhost:8000 with PostgreSQL database.

## Testing Strategy

**E2E Tests (tests/test_auth.py)**: verify authentication flows with Playwright browser automation.

**Integration Tests**: exercise registration and login through front-end pages with real browser interactions.

Run the full suite:

```bash
pytest tests/test_auth.py -v
```

Run with Playwright headed mode:

```bash
pytest tests/test_auth.py -v --headed
```

## Project Structure

```
assign 13 web api/
├── main.py                  # FastAPI application with auth endpoints
├── auth.py                  # JWT token generation and password hashing
├── database.py              # Database configuration and User model
├── schemas.py               # Pydantic validation schemas
├── static/
│   ├── register.html        # User registration page
│   └── login.html           # User login page
├── tests/
│   ├── conftest.py          # Pytest fixtures with Playwright setup
│   └── test_auth.py         # Playwright E2E authentication tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── README.md
└── REFLECTION.md
```

## API Endpoints

### Authentication Operations

**Register User:**

```http
POST /register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Login:**

```http
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123"
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**Health Check:**

```http
GET /health
```

## Pydantic Validation

The schemas.py module provides comprehensive validation:

**UserCreate Schema:**

- Email: Valid email format using EmailStr validator
- Username: 3-50 characters, alphanumeric with underscores/hyphens
- Password: Minimum 8 characters with at least one letter and one number

**UserLogin Schema:**

- Email: Valid email format
- Password: Required string

**Token Schema:**

- access_token: JWT token string
- token_type: Authentication type (bearer)

Example validation errors are caught and returned with appropriate HTTP status codes (422 Unprocessable Entity).

## JWT Authentication

JWT tokens are generated using the python-jose library with HS256 algorithm:

- Secret key configurable via environment variable
- Token expiration time configurable (default: 30 minutes)
- Tokens include user email and expiration timestamp
- Password verification using bcrypt with automatic salt generation

Security features:

- Passwords never stored in plain text
- Bcrypt hashing with automatic salt
- JWT tokens signed and verifiable
- Configurable token expiration

## Database Schema

**Users Table:**

- id (Integer, Primary Key)
- username (String, Unique, Indexed)
- email (String, Unique, Indexed)
- hashed_password (String)

All passwords are hashed using bcrypt before storage. Duplicate email/username detection prevents registration conflicts.

## Front-End Pages

### Registration Page (static/register.html)

- Email input with format validation
- Username input with length validation
- Password input with strength requirements display
- Confirm password with matching validation
- Real-time validation feedback
- Success/error message display

### Login Page (static/login.html)

- Email input
- Password input
- JWT token display on successful login
- Token stored in localStorage
- Success/error message display

Both pages feature:

- Modern gradient backgrounds
- Responsive design
- Client-side validation
- Server-side validation integration
- data-testid attributes for E2E testing

## Continuous Integration

The repository includes a GitHub Actions workflow (.github/workflows/ci-cd.yml) that runs on every push:

**Test Job:**

- Set up Python 3.11
- Start PostgreSQL 15 service container
- Install dependencies with caching
- Install Playwright with system dependencies
- Start FastAPI server in background
- Run Playwright E2E tests
- Upload test results as artifacts

**Build and Push Job (main branch only):**

- Build Docker image
- Tag with latest and commit SHA
- Push to Docker Hub (bhavanavuttunoori/jwt-auth-api)

**Required GitHub Secrets:**

- DOCKER_USERNAME: Your Docker Hub username
- DOCKER_PASSWORD: Your Docker Hub access token

## Assignment Instructions & Deliverables

**Objective:** Implement and test JWT authentication endpoints with user registration/login, front-end pages with validation, and comprehensive E2E testing with CI/CD pipeline.

### Implementation Checklist

- SQLAlchemy User model with password hashing
- Pydantic schemas with validation (email format, password strength)
- User registration endpoint with duplicate detection
- User login endpoint with JWT token generation
- Front-end registration page with client-side validation
- Front-end login page with token display
- Playwright E2E tests covering authentication flows
- FastAPI application with JWT authentication
- GitHub Actions workflow with PostgreSQL and Playwright
- Docker containerization with docker-compose support
- Comprehensive documentation

### Submission Package

- GitHub repository: https://github.com/BhavanaVuttunoori/ASSIGNMENT13
- Docker Hub image: https://hub.docker.com/r/bhavanavuttunoori/jwt-auth-api
- Screenshots demonstrating:
  - Successful GitHub Actions workflow
  - Docker Hub deployment
  - API documentation (Swagger UI)
  - User registration working
  - User login with JWT token
  - E2E tests passing

## Grading Guidelines

**Criterion: Authentication Endpoints (30 Points)**

- Registration endpoint with validation and password hashing
- Login endpoint with JWT token generation
- Proper error handling (duplicate users, invalid credentials)
- Password strength validation

**Criterion: Front-End Pages (20 Points)**

- Registration page with all required fields
- Login page with token display
- Client-side validation
- Success/error message handling

**Criterion: Pydantic Validation (15 Points)**

- Email format validation
- Password strength requirements
- Username length validation
- Proper error messages

**Criterion: E2E Testing (20 Points)**

- Playwright test suite with browser automation
- Positive and negative test scenarios
- UI element verification
- Error handling tests

**Criterion: CI/CD Pipeline (10 Points)**

- GitHub Actions workflow configuration
- PostgreSQL service container integration
- Playwright browser automation in CI
- Docker build and push automation

**Criterion: Documentation (5 Points)**

- Comprehensive README with setup instructions
- API documentation via Swagger
- Code comments and structure

## Helpful Commands

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Run application | `uvicorn main:app --reload` |
| Run all tests | `pytest tests/test_auth.py -v` |
| Run tests headed | `pytest tests/test_auth.py -v --headed` |
| Install Playwright | `playwright install chromium` |
| Build Docker image | `docker build -t jwt-auth-api .` |
| Run with Docker Compose | `docker-compose up -d` |
| Stop Docker Compose | `docker-compose down` |
| View container logs | `docker logs -f jwt_auth_app` |

## Submission Tips

- Commit frequently with meaningful messages describing each feature
- Keep .env or secrets out of version control (use .gitignore)
- Verify all tests pass locally before pushing
- Ensure GitHub Actions workflow completes successfully
- Capture required screenshots showing green checkmarks in Actions tab
- Verify Docker image is publicly accessible on Docker Hub
- Update README with your actual GitHub and Docker Hub usernames
- Test both registration and login flows manually

## Learning Outcomes

**CLO3: Create Python applications with automated testing**

- Comprehensive E2E tests with Playwright
- Browser automation for realistic testing
- Test fixtures and database isolation
- Front-end and back-end integration tests

**CLO4: Set up GitHub Actions for CI**

- Automated testing on push and pull requests
- PostgreSQL service containers
- Playwright browser automation in CI
- Automated Docker builds and deployment

**CLO9: Apply containerization techniques**

- Optimized Dockerfile for production
- Docker Compose for local development
- Environment variable management
- Service orchestration with health checks

**CLO10: Create, consume, and test REST APIs**

- RESTful endpoint design
- Proper HTTP methods and status codes
- API documentation with OpenAPI/Swagger
- Request/response validation

**CLO11: Integrate with SQL databases**

- SQLAlchemy ORM User model
- Database session management
- Unique constraints and indexing
- PostgreSQL in production

**CLO12: Serialize/deserialize JSON with Pydantic**

- Input validation schemas with custom validators
- Output serialization
- Type safety with Python type hints
- Email validation and password strength checks

**CLO13: Implement secure authentication**

- JWT token generation and validation
- Password hashing with bcrypt
- Secure password storage
- Token-based authentication
- Configurable token expiration

## Author

**Bhavana Vuttunoori**

- GitHub: https://github.com/BhavanaVuttunoori
- Repository: https://github.com/BhavanaVuttunoori/ASSIGNMENT13

## Acknowledgments

FastAPI documentation and community examples. SQLAlchemy ORM patterns and best practices. Pydantic validation framework. Playwright testing framework. python-jose for JWT implementation. GitHub Actions workflow templates. Course instructors for project guidance.

## Support

For questions or issues:

- Check the GitHub Issues: https://github.com/BhavanaVuttunoori/ASSIGNMENT13/issues
- Review the API documentation at http://localhost:8000/docs
- Contact the repository maintainer

## License

This project is created as part of Assignment 13 for demonstrating JWT authentication, Pydantic validation, front-end integration, E2E testing with Playwright, and CI/CD pipelines.

---

**Note:** This project was created as part of Assignment 13 for demonstrating secure JWT authentication, comprehensive validation with Pydantic, front-end pages with client-side validation, Playwright E2E testing, and automated CI/CD pipelines.
