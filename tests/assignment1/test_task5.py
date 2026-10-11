
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
@pytest.mark.smoke
async def test_website_navigation(async_page):
    # Open the configured website
    await async_page.goto("https://www.google.com/")

    # Verify the website title
    await expect(async_page).to_have_title("Google")

    # Verify that navigation reached the expected domain
    assert "google.com" in async_page.url
