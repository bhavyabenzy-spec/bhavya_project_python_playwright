
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_checkout_journey(async_page):

    # Step 1: Open Amazon India
    await async_page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    # Step 2: Search for a book
    search_box = async_page.locator("#twotabsearchtextbox")
    await search_box.fill("Book")
    await search_box.press("Enter")

    # Step 3: Wait for search results
    product_cards = async_page.locator(
        "div[data-component-type='s-search-result']"
    )

    await expect(product_cards.first).to_be_visible(
        timeout=20000
    )

    # Step 4: Print the first product title
    product_title = (
        await product_cards.first.locator("h2").inner_text()
    ).strip()

    print("Selected product:", product_title)

    # Step 5: Find the product link
    product_link = async_page.locator(
        ".s-asin a:has(h2)"
    ).first

    await expect(product_link).to_be_visible(timeout=15000)

    # Step 6: Click the book and capture the new tab
    async with async_page.expect_popup() as popup_info:
        await product_link.click()

    product_page = await popup_info.value

    # Wait for the book page to load
    await product_page.wait_for_load_state("domcontentloaded")

    # Step 7: Verify the product title on the new tab
    product_title_on_page = product_page.locator("#productTitle")

    await expect(product_title_on_page).to_be_visible(
        timeout=20000
    )

    actual_title = (
        await product_title_on_page.inner_text()
    ).strip()

    print("Book details page:", actual_title)

    # Step 8: Verify the Add to Cart button
    add_to_cart = product_page.locator("#add-to-cart-button")

    await expect(add_to_cart).to_be_visible(timeout=15000)

    print("Add to Cart button is visible.")
    print("Checkout journey verification completed.")
    print("No item added to cart and no order placed.")
