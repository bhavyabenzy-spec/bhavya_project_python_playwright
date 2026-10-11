
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_typing_and_keyboard_actions():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://demowebshop.tricentis.com/")

        # 1. Locate the search input
        search_box = page.locator("#small-searchterms")

        # 2. Enter data using fill()
        await search_box.fill("computer")
        await expect(search_box).to_have_value("computer")

        # 3. Press Enter to search
        await search_box.press("Enter")

        # Verify that the search results page is displayed
        await expect(page).to_have_url(
            "https://demowebshop.tricentis.com/search?q=computer"
        )

        # 4. Clear and replace the existing value
        search_box = page.locator("#Q")

        await search_box.fill("laptop")
        await expect(search_box).to_have_value("laptop")

        # 5. Demonstrate a keyboard shortcut: Ctrl+A
        await search_box.press("Control+A")

        # Replace the selected text
        await search_box.fill("phone")

        # 6. Validate the final input value
        await expect(search_box).to_have_value("phone")

        print("Typing and keyboard actions completed successfully")

        await browser.close()
