import pytest
from playwright.async_api import async_playwright, expect
import asyncio


#Create a basic test that launches a browser, opens a website, and validates the page title
@pytest.mark.asyncio
@pytest.mark.smoke
async def test_printTitle():
    async with async_playwright() as p:
      browser = await p.chromium.launch(headless=False)
      user_context= await browser.new_context()
      page= await user_context.new_page()
      await page.goto('https://facebook.com/')
      print(await page.title())
      await expect(page).to_have_title("Facebook")