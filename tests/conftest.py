import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context for all tests
    """
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        },
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="function")
def page():
    """
    Provide a Playwright page for each test
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            ignore_https_errors=True
        )
        page = context.new_page()
        
        # Clear localStorage before test
        page.goto("http://localhost:8000/static/login.html")
        page.evaluate("() => localStorage.clear()")
        
        yield page
        
        # Cleanup
        page.evaluate("() => localStorage.clear()")
        context.close()
        browser.close()
