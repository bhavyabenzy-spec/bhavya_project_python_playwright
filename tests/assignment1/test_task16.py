import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_dynamic_waits():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. Open SauceDemo
        await page.goto("https://www.saucedemo.com/")

        # 2. Login
        await page.locator('[data-test="username"]').fill("standard_user")
        await page.locator('[data-test="password"]').fill("secret_sauce")
        await page.locator('[data-test="login-button"]').click()

        # 3. Wait for the inventory page
        await expect(page).to_have_url(
            "https://www.saucedemo.com/inventory.html"
        )

        # 4. Locate the first product's Add to cart button
        add_to_cart = page.locator(
            '[data-test="add-to-cart-sauce-labs-backpack"]'
        )

        # 5. Trigger the dynamic update
        await add_to_cart.click()

        # 6. Wait for the cart badge to become visible
        cart_badge = page.locator(
            '[data-test="shopping-cart-badge"]'
        )
        await expect(cart_badge).to_be_visible()

        # 7. Validate the updated cart count
        await expect(cart_badge).to_have_text("1")

        # 8. Verify the button changed to Remove
        remove_button = page.locator(
            '[data-test="remove-sauce-labs-backpack"]'
        )
        await expect(remove_button).to_be_visible()

        print("Dynamic cart update verified successfully!")

        await browser.close()