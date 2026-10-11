import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_soft_assertions():

    failures = []

    async def soft_check(description, assertion):
        try:
            await assertion
            print(f"PASSED: {description}")

        except AssertionError as error:
            failures.append(f"{description}: {error}")
            print(f"FAILED: {description}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.saucedemo.com/")

        # 1. Verify page title
        await soft_check(
            "Page title",
            expect(page).to_have_title("Swag Labs")
        )

        # 2. Verify username field visibility
        username = page.locator('[data-test="username"]')
        await soft_check(
            "Username visibility",
            expect(username).to_be_visible()
        )

        # 3. Verify login button text
        login_button = page.locator('[data-test="login-button"]')

        # Intentional failure for learning purposes
        await soft_check(
            "Login button text",
             expect(login_button).to_have_text("Login")        )

        # 4. Verify password field visibility
        password = page.locator('[data-test="password"]')
        await soft_check(
            "Password visibility",
            expect(password).to_be_visible()
        )

        # 5. Verify login button is enabled
        await soft_check(
            "Login button enabled",
            expect(login_button).to_be_enabled()
        )

        await browser.close()

    # Report all failures at the end
    if failures:
        pytest.fail(
            "\nSoft assertion failures:\n"
            + "\n".join(failures)
        )
