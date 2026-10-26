
import os
import re
from pathlib import Path

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

import config


# Get the project root folder.
# This file is inside tests/assignment4-24OCTto30OCT-Bhavya/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Folder where failure screenshots will be saved
SCREENSHOT_DIR = PROJECT_ROOT / "artifacts" / "screenshots"


# --------------------------------------------------
# FIXTURE 1: Base URL
# Scope: session
# The base URL is configuration, so it can be reused
# throughout the test session.
# --------------------------------------------------
@pytest.fixture(scope="session")
def base_url():
    return os.getenv(
        "BASE_URL",
        getattr(config, "BASE_URL", "https://demowebshop.tricentis.com/")
    )


# --------------------------------------------------
# FIXTURE 2: Browser
# Scope: function
# Each test gets its own browser for isolation.
# --------------------------------------------------
@pytest_asyncio.fixture
async def browser(request):
    browser_names = request.config.getoption("--browser")
    browser_name = browser_names[0] if browser_names else "chromium"

    async with async_playwright() as playwright:
        browser_type = getattr(playwright, browser_name)

        browser_instance = await browser_type.launch(
            headless=config.HEADLESS
        )

        try:
            yield browser_instance
        finally:
            await browser_instance.close()


# --------------------------------------------------
# FIXTURE 3: Browser context
# Scope: function
# Each test gets a separate context, so cookies and
# browser storage do not leak between tests.
# --------------------------------------------------
@pytest_asyncio.fixture
async def context(browser):
    browser_context = await browser.new_context()

    try:
        yield browser_context
    finally:
        await browser_context.close()


# --------------------------------------------------
# FIXTURE 4: Page
# Scope: function
# Creates a page and captures a screenshot if the
# test fails. The screenshot is taken before the
# context and browser are closed.
# --------------------------------------------------
@pytest_asyncio.fixture
async def async_page(context, request):
    page = await context.new_page()

    page.set_default_timeout(config.DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(config.NAVIGATION_TIMEOUT)

    try:
        yield page
    finally:
        report = getattr(request.node, "rep_call", None)

        if report and report.failed and not page.is_closed():
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

            # Make the test name safe for use as a filename
            safe_name = re.sub(
                r"[^a-zA-Z0-9_-]",
                "_",
                request.node.name
            )

            screenshot_path = SCREENSHOT_DIR / f"{safe_name}.png"

            try:
                await page.screenshot(path=str(screenshot_path))
                print(f"\nFailure screenshot saved: {screenshot_path}")
            except Exception as error:
                print(f"\nCould not capture screenshot: {error}")


# --------------------------------------------------
# FIXTURE 5: Authenticated storage state
# Reads the saved browser state from Task 4, if present.
# --------------------------------------------------
@pytest.fixture(scope="session")
def authenticated_storage_state():
    state_file = PROJECT_ROOT / ".auth" / "state.json"

    if state_file.exists():
        return str(state_file)

    return None


# --------------------------------------------------
# FIXTURE 6: Authenticated context
# Creates a context using the saved state.
# Tests that need it must request this fixture.
# --------------------------------------------------
@pytest_asyncio.fixture
async def authenticated_context(browser, authenticated_storage_state):
    if authenticated_storage_state is None:
        pytest.skip(
            "Saved browser state not found. Run Task 4 first."
        )

    browser_context = await browser.new_context(
        storage_state=authenticated_storage_state
    )

    try:
        yield browser_context
    finally:
        await browser_context.close()


# --------------------------------------------------
# PYTEST HOOK: Save the result of each test phase.
# The page fixture uses the call-phase result to
# determine whether a screenshot is needed.
# --------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    setattr(item, f"rep_{report.when}", report)
