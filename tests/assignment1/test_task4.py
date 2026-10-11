
import pytest
from playwright.async_api import expect
import config


# Test using the reusable fixture
@pytest.mark.asyncio
async def test_configuration(async_page):

    # Open the configured website
    await async_page.goto(config.BASE_URL)

    # Print the current page title
    print("Page title:", await async_page.title())

    # Verify the title using config.py
    await expect(async_page).to_have_title(
        config.EXPECTED_TITLE
    )
