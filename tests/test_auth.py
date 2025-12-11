import pytest
from playwright.sync_api import Page, expect
import time


def test_login_with_correct_credentials(page: Page):
    """
    Positive Test: Login with correct credentials
    First registers a user, then logs in with those credentials
    """
    # First, register a new user
    page.goto("http://localhost:8000/static/register.html")
    
    timestamp = int(time.time())
    email = f"logintest{timestamp}@example.com"
    username = f"logintest{timestamp}"
    password = "LoginPass123"
    
    page.fill('[data-testid="email-input"]', email)
    page.fill('[data-testid="username-input"]', username)
    page.fill('[data-testid="password-input"]', password)
    page.fill('[data-testid="confirm-password-input"]', password)
    page.click('[data-testid="register-button"]')
    
    # Wait a moment for registration to complete
    page.wait_for_timeout(3000)
    
    # Navigate to login page
    page.goto("http://localhost:8000/static/login.html")
    
    # Fill in login form
    page.fill('[data-testid="email-input"]', email)
    page.fill('[data-testid="password-input"]', password)
    
    # Click login button
    page.click('[data-testid="login-button"]')
    
    # Verify token is displayed (indicating successful login)
    token_display = page.locator("#tokenDisplay")
    expect(token_display).to_be_visible(timeout=10000)


def test_login_with_wrong_password(page: Page):
    """
    Negative Test: Login with incorrect password
    First registers a user, then attempts login with wrong password
    """
    # Register a user first
    page.goto("http://localhost:8000/static/register.html")
    
    timestamp = int(time.time())
    email = f"wrongpass{timestamp}@example.com"
    username = f"wrongpass{timestamp}"
    correct_password = "CorrectPass123"
    
    page.fill('[data-testid="email-input"]', email)
    page.fill('[data-testid="username-input"]', username)
    page.fill('[data-testid="password-input"]', correct_password)
    page.fill('[data-testid="confirm-password-input"]', correct_password)
    page.click('[data-testid="register-button"]')
    
    # Wait for registration
    page.wait_for_timeout(2000)
    
    # Navigate to login page
    page.goto("http://localhost:8000/static/login.html")
    
    # Try to login with wrong password
    page.fill('[data-testid="email-input"]', email)
    page.fill('[data-testid="password-input"]', "WrongPassword123")
    page.click('[data-testid="login-button"]')
    
    # Check for error message indicating invalid credentials
    general_error = page.locator("#generalError")
    expect(general_error).to_be_visible(timeout=5000)
    expect(general_error).to_contain_text("Invalid email or password")
    
    # Verify token is NOT displayed
    token_display = page.locator("#tokenDisplay")
    expect(token_display).not_to_be_visible()


def test_login_with_nonexistent_user(page: Page):
    """
    Negative Test: Login with email that doesn't exist
    Tests server response for non-existent user
    """
    page.goto("http://localhost:8000/static/login.html")
    
    # Use an email that definitely doesn't exist
    nonexistent_email = f"nonexistent{int(time.time())}@example.com"
    password = "SomePassword123"
    
    page.fill('[data-testid="email-input"]', nonexistent_email)
    page.fill('[data-testid="password-input"]', password)
    page.click('[data-testid="login-button"]')
    
    # Check for error message
    general_error = page.locator("#generalError")
    expect(general_error).to_be_visible(timeout=5000)
    expect(general_error).to_contain_text("Invalid email or password")


def test_ui_elements_present_register(page: Page):
    """
    Test: Verify all UI elements are present on registration page
    """
    page.goto("http://localhost:8000/static/register.html")
    
    # Check for form elements
    expect(page.locator('[data-testid="email-input"]')).to_be_visible()
    expect(page.locator('[data-testid="username-input"]')).to_be_visible()
    expect(page.locator('[data-testid="password-input"]')).to_be_visible()
    expect(page.locator('[data-testid="confirm-password-input"]')).to_be_visible()
    expect(page.locator('[data-testid="register-button"]')).to_be_visible()
    
    # Check for password requirements
    expect(page.locator("#req-length")).to_be_visible()
    expect(page.locator("#req-letter")).to_be_visible()
    expect(page.locator("#req-number")).to_be_visible()


def test_ui_elements_present_login(page: Page):
    """
    Test: Verify all UI elements are present on login page
    """
    page.goto("http://localhost:8000/static/login.html")
    
    # Check for form elements
    expect(page.locator('[data-testid="email-input"]')).to_be_visible()
    expect(page.locator('[data-testid="password-input"]')).to_be_visible()
    expect(page.locator('[data-testid="login-button"]')).to_be_visible()
