import pytest
from playwright.async_api import async_playwright, expect
import config
import os

@pytest.mark.asyncio
async def test_locator_strategies():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        base_url = os.getenv("SAUCE_BASE_URL")
        username = os.getenv("SAUCE_USERNAME")
        password = os.getenv("SAUCE_PASSWORD")

        await page.goto(base_url)

        # Locate the username field using its placeholder
        username_placeholder = page.get_by_placeholder("Username")

        # Verify that the field is visible
        await expect(username_placeholder).to_be_visible()

        # Enter the username
        await username_placeholder.fill(username)

        # Verify the entered username
        await expect(username_placeholder).to_have_value(username)

        # Continue with the other locator strategies
        await page.locator("//input[@id='password']").fill(password)
        await expect(page.locator("//input[@id='password']")).to_have_value(password)

        # CSS selector: click Login
        await page.locator("#login-button").click()

        # Verify successful login
        await expect(page).to_have_url(base_url + "inventory.html")

        # Visible text: open a product
        await page.get_by_text("Sauce Labs Backpack", exact=True).click()

        # Verify product details
        await expect(page.locator(".inventory_details_name")).to_have_text(
            "Sauce Labs Backpack"
        )

        # Role locator: add the product to the cart
        await page.get_by_role("button", name="Add to cart").click()

        # Verify the button changes to Remove
        await expect(
            page.get_by_role("button", name="Remove")
        ).to_be_visible()

        await browser.close()