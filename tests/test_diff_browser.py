import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_diff_browser():

    async with async_playwright() as p:

        chromeBrowser = await p.chromium.launch(headless=False)

        user_context = await chromeBrowser.new_context()
        page = await user_context.new_page()
        await page.goto("https://google.com")

        admin_context = await chromeBrowser.new_context()
        page = await admin_context.new_page()
        await page.goto("https://example.com/")

        await chromeBrowser.close()

        fireFoxBrowser = await p.firefox.launch(headless=False)

        user_context = await fireFoxBrowser.new_context()
        page = await user_context.new_page()
        await page.goto("https://google.com")

        admin_context = await fireFoxBrowser.new_context()
        page = await admin_context.new_page()
        await page.goto("https://example.com/")

        await chromeBrowser.close()

        