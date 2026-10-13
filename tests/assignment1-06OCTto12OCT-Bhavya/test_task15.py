import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_waits():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. Wait for DOM content to be loaded
        await page.goto(
            "https://www.saucedemo.com/",
            wait_until="domcontentloaded"
        )

        # 2. Locate the username field
        username = page.locator('[data-test="username"]')

        # 3. Wait until the username field is visible
        await username.wait_for(state="visible")

        # 4. Interact with the username field
        # Playwright automatically waits for the field to be ready
        await username.fill("standard_user")

        # 5. Enter the password
        password = page.locator('[data-test="password"]')
        await password.fill("secret_sauce")

        # 6. Click the login button
        # Playwright auto-waits before clicking
        login_button = page.locator('[data-test="login-button"]')
        await login_button.click()

        # 7. Wait for the URL condition
        await page.wait_for_url("**/inventory.html")

        # 8. Verify that the inventory page is displayed
        await expect(page).to_have_url(
            "https://www.saucedemo.com/inventory.html"
        )

        # 9. Wait for the first product to become visible
        products = page.locator(".inventory_item_name")
        await products.first.wait_for(state="visible")

        # 10. Verify that all six products are displayed
        await expect(products).to_have_count(6)

        print("All wait checks passed!")

        await browser.close()