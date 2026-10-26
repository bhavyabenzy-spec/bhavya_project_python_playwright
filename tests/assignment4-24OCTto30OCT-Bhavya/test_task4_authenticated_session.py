
from pathlib import Path

import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_save_and_reuse_browser_storage_state(async_page):
    page = async_page

    # STEP 1: Open Demo Web Shop
    await page.goto("https://demowebshop.tricentis.com/")

    await expect(
        page.get_by_role("link", name="Tricentis Demo Web Shop")
    ).to_be_visible()

    print("Step 1: Demo Web Shop opened.")

    # STEP 2: Create the folder for the saved browser state
    state_file = Path(".auth/state.json")
    state_file.parent.mkdir(parents=True, exist_ok=True)

    # STEP 3: Add a test cookie and local-storage value
    # These are test values, not real login credentials.
    await page.evaluate("""
        () => {
            document.cookie =
                "assignment4_test_cookie=saved_cookie_value; path=/; SameSite=Lax";

            localStorage.setItem(
                "assignment4_test_key",
                "saved_local_storage_value"
            );
        }
    """)

    print("Step 2: Test cookie and local-storage value created.")

    # STEP 4: Save cookies and local storage to a JSON file
    await page.context.storage_state(path=str(state_file))

    assert state_file.exists(), "Browser state file was not created."

    print("Step 3: Browser storage state saved.")

    # STEP 5: Get the browser used by the existing fixture
    browser = page.context.browser()
    assert browser is not None, "Could not access the browser."

    # STEP 6: Open a new context using the saved state
    new_context = await browser.new_context(
        storage_state=str(state_file)
    )

    try:
        new_page = await new_context.new_page()

        # Open the same website origin so local storage is available
        await new_page.goto("https://demowebshop.tricentis.com/")

        # STEP 7: Verify that the local-storage value was restored
        saved_local_value = await new_page.evaluate(
            "() => localStorage.getItem('assignment4_test_key')"
        )

        assert saved_local_value == "saved_local_storage_value"

        print("Step 4: Local-storage value restored successfully.")

        # STEP 8: Verify that the cookie was restored
        cookies = await new_context.cookies(
            "https://demowebshop.tricentis.com/"
        )

        cookie_values = {
            cookie["name"]: cookie["value"]
            for cookie in cookies
        }

        assert (
            cookie_values.get("assignment4_test_cookie")
            == "saved_cookie_value"
        ), "Test cookie was not restored."

        print("Step 5: Cookie restored successfully.")

        # Verify that the website opened in the new context
        await expect(
            new_page.get_by_role(
                "link", name="Tricentis Demo Web Shop"
            )
        ).to_be_visible()

        print("Task 4: Browser storage reuse verified.")

    finally:
        # Always close the new context
        await new_context.close()
