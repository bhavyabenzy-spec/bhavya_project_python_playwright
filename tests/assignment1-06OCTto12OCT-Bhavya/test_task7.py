import pytest
from playwright.async_api import async_playwright, expect
import config


@pytest.mark.asyncio
async def test_secure_login():

    # Check credentials without printing them
    assert config.TEST_USERNAME
    assert config.TEST_PASSWORD

    print("Selected Environment:", config.ENV_NAME)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Open Demo Web Shop
        await page.goto(config.BASE_URL)

        # Open the login page
        await page.get_by_role("link", name="Log in").click()

        # Enter credentials from .env
        await page.locator("#Email").fill(config.TEST_USERNAME)
        await page.locator("#Password").fill(config.TEST_PASSWORD)

        # Click the login button
        await page.locator("input.login-button").click()

        # Verify that login succeeded
        await expect(
            page.get_by_role("link", name="Log out")
        ).to_be_visible(timeout=10000)

        print("Login verification passed")

        await browser.close()