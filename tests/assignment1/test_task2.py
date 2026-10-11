import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, expect


# Launch a browser, open a website, and validate the title.
@pytest.mark.asyncio
@pytest.mark.regression
async def test_open_website():
    async with async_playwright() as p:
        # Launch Chromium in headed mode
        browser = await p.chromium.launch(headless=False)

        # Create a browser context
        user_context = await browser.new_context()

        # Create a page inside the context
        page = await user_context.new_page()

        # Open Facebook
        await page.goto("https://www.facebook.com/")

        # Print and verify the page title
        print("Page title:", await page.title())
        await expect(page).to_have_title("Facebook")

        # Close the browser
        await browser.close()



# Create a custom fixture that creates a new browser context.

@pytest.fixture
async def custom_context():
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=False)

        # Create a new browser context
        context = await browser.new_context()

        # Provide the context to the test
        yield context

        # Close the context and browser after the test
        await context.close()
        await browser.close()



# Create a fixture that returns a page from the custom context.


# Create a page from the custom context
@pytest_asyncio.fixture
async def custom_page(custom_context):
    # Create a new page inside the context
    page = await custom_context.new_page()

    # Provide the page to the test
    yield page

    # Close the page after the test
    await page.close()




# Create a custom asynchronous browser context
@pytest_asyncio.fixture
async def custom_context():
    async with async_playwright() as p:
        # Launch Chromium
        browser = await p.chromium.launch(headless=False)

        # Create a new browser context
        context = await browser.new_context()

        # Provide the context to the test
        yield context

        # Clean up after the test
        await context.close()
        await browser.close()



# TASK 12:
# Demonstrate that cookies are isolated between browser contexts.

@pytest.mark.asyncio
async def test_first_context():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.google.com/")

        # Add a cookie to the first context
        await context.add_cookies([
            {
                "name": "test_cookie",
                "value": "first_test",
                "url": "https://www.google.com/"
            }
        ])

        # Read cookies from the first context
        cookies = await context.cookies()
        print("First context cookies:", cookies)

        # Confirm that our cookie exists
        assert any(
            cookie["name"] == "test_cookie"
            for cookie in cookies
        )

        await browser.close()


@pytest.mark.asyncio
async def test_second_context():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.google.com/")

        # Read cookies from the second, separate context
        cookies = await context.cookies()
        print("Second context cookies:", cookies)

        # Confirm that the first context's cookie is absent
        assert not any(
            cookie["name"] == "test_cookie"
            for cookie in cookies
        )

        await browser.close()
