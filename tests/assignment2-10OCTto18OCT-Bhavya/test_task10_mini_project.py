
import re
import pytest
from playwright.async_api import expect


# Product we want to find on Amazon
PRODUCT = "Atomic Habits: Tiny Changes, Remarkable Results"


# Helper 1: Search for the product
async def search_product(page):
    await page.goto("https://www.amazon.in/")

    search_box = page.locator("#twotabsearchtextbox")
    await search_box.fill("Atomic Habits")
    await search_box.press("Enter")

    # Wait until Amazon displays the search results
    results = page.locator(
        "div[data-component-type='s-search-result']"
    )

    await expect(results.first).to_be_visible(timeout=15000)


# Helper 2: Find the product card by its visible title
async def get_product_card(page):
    product_heading = page.get_by_text(
        PRODUCT,
        exact=False
    ).first

    await expect(product_heading).to_be_visible(timeout=15000)

    # Find the result card containing the product title
    product_card = product_heading.locator(
        "xpath=ancestor::div[@data-component-type='s-search-result']"
    )

    await expect(product_card).to_be_visible()
    return product_card


# Test 1: Verify Amazon search results
@pytest.mark.asyncio
async def test_product_search(async_page):
    await search_product(async_page)

    results = async_page.locator(
        "div[data-component-type='s-search-result']"
    )

    assert await results.count() > 0, (
        "Amazon search did not return any products."
    )


# Test 2: Verify the correct product card
@pytest.mark.asyncio
async def test_correct_product_card(async_page):
    await search_product(async_page)

    product_card = await get_product_card(async_page)

    # Check that the selected card contains the expected product
    await expect(product_card).to_contain_text(
        PRODUCT,
        timeout=10000
    )


# Test 3: Verify the product link
@pytest.mark.asyncio
async def test_product_link(async_page):
    await search_product(async_page)

    product_card = await get_product_card(async_page)

    # Find the product link inside the selected card
    product_link = product_card.locator(
        "a[href*='/dp/']"
    ).first

    await expect(product_link).to_be_visible()

    # Verify that the link points to an Amazon product page
    await expect(product_link).to_have_attribute(
        "href",
        re.compile(r"/dp/")
    )


# Test 4: Open and verify product details in a new tab
@pytest.mark.asyncio
async def test_product_details(async_page):
    await search_product(async_page)

    product_card = await get_product_card(async_page)

    product_link = product_card.locator(
        "a[href*='/dp/']"
    ).first

    # Capture the new tab when the product link is clicked
    async with async_page.expect_popup() as popup_info:
        await product_link.click()

    detail_page = await popup_info.value

    # Verify the product title in the new tab
    try:
        product_title = detail_page.locator("#productTitle")

        await expect(product_title).to_be_visible(timeout=15000)

        actual_title = (await product_title.inner_text()).strip()

        assert "Atomic Habits" in actual_title, (
            f"Unexpected product title: {actual_title}"
        )

        print(f"\nVerified product details: {actual_title}")

    finally:
        # Close the popup after verification
        await detail_page.close()
