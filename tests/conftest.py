
import pytest_asyncio
from playwright.async_api import async_playwright
import config


@pytest_asyncio.fixture
async def async_page(request):
    async with async_playwright() as p:

        # Get the browser names supplied through --browser
        browser_names = request.config.getoption("--browser")

        # Select the first browser for this fixture instance
        browser_name = browser_names[0]

        # Select Chromium, Firefox, or WebKit
        browser_type = getattr(p, browser_name)

        # Launch the selected browser
        browser = await browser_type.launch(
            headless=config.HEADLESS
        )

        # Create a new context and page
        context = await browser.new_context()
        page = await context.new_page()

        # Apply configured timeouts
        page.set_default_timeout(config.DEFAULT_TIMEOUT)
        page.set_default_navigation_timeout(
            config.NAVIGATION_TIMEOUT
        )

        yield page

        # Clean up
        await context.close()
        await browser.close()
