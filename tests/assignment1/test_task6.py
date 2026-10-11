import pytest
from playwright.async_api import async_playwright
import config


@pytest.mark.asyncio
async def test_environment_url():

    # Print the selected environment
    print("Selected Environment:", config.ENV_NAME)

    # Print the URL (not any password or secret)
    print("Test URL:", config.BASE_URL)

    # Start Playwright
    async with async_playwright() as p:

        # Launch Chromium browser
        browser = await p.chromium.launch(headless=False)

        # Create a new page
        page = await browser.new_page()

        # Open the URL for the selected environment
        response = await page.goto(config.BASE_URL)

        # Check that the page loaded successfully
        assert response is not None
        assert response.status < 400

        # Print the actual URL opened in the browser
        print("Actual Page URL:", page.url)

        # Close the browser
        await browser.close()