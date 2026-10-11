import pytest
from playwright.async_api import (
    async_playwright,
    expect,
    TimeoutError as PlaywrightTimeoutError
)


@pytest.mark.asyncio
async def test_timeout_handling():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. Configure default timeouts
        page.set_default_timeout(5000)

        # 2. Configure navigation timeout separately
        page.set_default_navigation_timeout(10000)

        await page.goto("https://www.saucedemo.com/")

        # 3. Intentionally wait for a missing element
        missing_element = page.locator("#missing-element")

        try:
            await missing_element.wait_for(
                state="visible",
                timeout=1500
            )

        except PlaywrightTimeoutError:
            print(
                "Expected timeout: missing element "
                "did not become visible within 1.5 seconds."
            )

        # 4. Login to SauceDemo
        await page.locator(
            '[data-test="username"]'
        ).fill("standard_user")

        await page.locator(
            '[data-test="password"]'
        ).fill("secret_sauce")

        await page.locator(
            '[data-test="login-button"]'
        ).click()

        await expect(page).to_have_url(
            "https://www.saucedemo.com/inventory.html"
        )

        # 5. Trigger a dynamic update
        add_to_cart = page.locator(
            '[data-test="add-to-cart-sauce-labs-backpack"]'
        )

        await add_to_cart.click()

        # 6. Custom wait condition: cart badge must equal 1
        try:
            await page.wait_for_function(
                """() => {
                    const badge = document.querySelector(
                        '[data-test="shopping-cart-badge"]'
                    );

                    return badge &&
                           badge.textContent.trim() === '1';
                }""",
                timeout=5000
            )

        except PlaywrightTimeoutError:
            pytest.fail(
                "Cart badge did not update to '1' "
                "within 5 seconds after clicking Add to cart."
            )

        # 7. Verify the final dynamic state
        cart_badge = page.locator(
            '[data-test="shopping-cart-badge"]'
        )

        await expect(cart_badge).to_have_text("1")

        print("Custom wait condition passed!")

        await browser.close()