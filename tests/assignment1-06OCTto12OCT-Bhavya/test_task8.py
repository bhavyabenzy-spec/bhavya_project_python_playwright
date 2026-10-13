import os
import pytest
from playwright.async_api import async_playwright, expect
import config


@pytest.mark.asyncio
async def test_core_navigation():

    # Read SauceDemo configuration and credentials
    base_url = os.getenv("SAUCE_BASE_URL")
    username = os.getenv("SAUCE_USERNAME")
    password = os.getenv("SAUCE_PASSWORD")

    # Check that required values are available
    assert base_url, "SAUCE_BASE_URL is missing"
    assert username, "SAUCE_USERNAME is missing"
    assert password, "SAUCE_PASSWORD is missing"

    async with async_playwright() as p:

        # Launch the browser
        browser = await p.chromium.launch(headless=False)

        try:
            page = await browser.new_page()

            # 1. Navigate to SauceDemo
            await page.goto(base_url)

            # 2. Validate the login page URL and title
            await expect(page).to_have_url(base_url)
            await expect(page).to_have_title("Swag Labs")

            print("Login page opened successfully")

            # 3. Locate username and password fields
            username_field = page.locator("#user-name")
            password_field = page.locator("#password")

            await expect(username_field).to_be_visible()
            await expect(password_field).to_be_visible()

            # 4. Enter credentials from .env
            await username_field.fill(username)
            await password_field.fill(password)

            # 5. Click the Login button
            await page.locator("#login-button").click()

            # 6. Verify successful login
            await expect(page).to_have_url(
                base_url + "inventory.html"
            )
            await expect(page).to_have_title("Swag Labs")
            await expect(
                page.get_by_text("Products", exact=True)
            ).to_be_visible()

            print("Login successful")

            # 7. Open a product

            await page.locator(".inventory_item_name").filter(
                has_text="Sauce Labs Backpack"
            ).click()

            # Verify that the product details page opened
            await expect(page).to_have_url(
                base_url + "inventory-item.html?id=4"
            )

            # Verify the product name
            await expect(
                page.locator(".inventory_details_name")
            ).to_have_text("Sauce Labs Backpack")

            print("Product details opened")

            # 8. Navigate backward
            await page.go_back()

            await expect(page).to_have_url(
                base_url + "inventory.html"
            )
            await expect(
                page.get_by_text("Products", exact=True)
            ).to_be_visible()

            print("Browser back navigation passed")

            # Navigate forward
            await page.go_forward()

            await expect(page).to_have_url(
                base_url + "inventory-item.html?id=4"
            )

            print("Browser forward navigation passed")

            # Reload the product page
            await page.reload()

            await expect(page).to_have_url(
                base_url + "inventory-item.html?id=4"
            )
            await expect(
                page.get_by_text("Sauce Labs Backpack", exact=True)
            ).to_be_visible()

            print("Page reload passed")

            

        finally:
            # Always close the browser
            await browser.close()