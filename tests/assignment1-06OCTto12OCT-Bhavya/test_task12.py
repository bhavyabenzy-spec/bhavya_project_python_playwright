import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_assertions():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Open the website
        await page.goto("https://www.saucedemo.com/")

        # 1. Verify page title
        await expect(page).to_have_title("Swag Labs")

        # 2. Verify URL
        await expect(page).to_have_url("https://www.saucedemo.com/")

        # 3. Verify element visibility
        username = page.locator('[data-test="username"]')
        await expect(username).to_be_visible()

        # 4. Verify element text
        login_button = page.locator('[data-test="login-button"]')
        await expect(login_button).to_have_text("Login")

        # 5. Verify input value
        await expect(username).to_have_value("")

        # 6. Verify element is enabled
        await expect(login_button).to_be_enabled()

        # Example of checking a disabled element:
        # await expect(some_element).to_be_disabled()

        # 7. Use pytest assert for a calculation
        price = 1200
        tax = 300
        total = price + tax

        assert total == 1500

        print("All assertions passed!")

        await browser.close()