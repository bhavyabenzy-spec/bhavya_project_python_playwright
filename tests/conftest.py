import pytest
from playwright.async_api import async_playwright
import pytest_asyncio

@pytest_asyncio.fixture
async def async_page():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=False)
        page= await browser.new_page()
        yield page
        await browser.close()

@pytest_asyncio.fixture
async def chromium_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False
        )
        context = await browser.new_context()

        pag = await context.new_page()
        