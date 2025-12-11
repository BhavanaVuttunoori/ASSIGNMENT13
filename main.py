from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import uvicorn

from database import get_db, init_db, User
from schemas import UserCreate, UserLogin, Token, UserResponse, MessageResponse
from auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# Initialize FastAPI app
app = FastAPI(
    title="JWT Authentication API",
    description="API with JWT-based authentication for user registration and login",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for front-end
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "JWT Authentication API",
        "endpoints": {
            "register": "/register",
            "login": "/login",
            "docs": "/docs",
            "registration_page": "/static/register.html",
            "login_page": "/static/login.html"
        }
    }


@app.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **email**: Valid email address (must be unique)
    - **username**: Username (3-50 characters, alphanumeric, must be unique)
    - **password**: Password (minimum 8 characters, must contain letters and digits)
    
    Returns success message on successful registration
    """
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create new user
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return MessageResponse(
        message="User registered successfully",
        detail=f"User {user.username} has been created"
    )


@app.post("/login", response_model=Token, tags=["Authentication"])
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns JWT access token on successful authentication
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    # Check if user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "username": user.username},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=UserResponse, tags=["Users"])
async def get_current_user(token: str, db: Session = Depends(get_db)):
    """
    Get current user information (protected endpoint example)
    
    Requires valid JWT token in query parameter
    """
    from auth import verify_token
    
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
