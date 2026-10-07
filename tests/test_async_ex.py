import pytest


@pytest.mark.asyncio
async def test_for_async(async_page):
    await async_page.goto("https://example.com/")