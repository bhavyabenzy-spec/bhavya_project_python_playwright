import re
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_product_discovery(async_page):

    # Step 1: Open Amazon India
    await async_page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    # Step 2: Search for a product using the keyword "Book"
    search_box = async_page.locator("#twotabsearchtextbox")

    await expect(search_box).to_be_visible(timeout=15000)
    await search_box.fill("Book")
    await search_box.press("Enter")

    # Step 3: Wait for search results
    await async_page.wait_for_load_state("domcontentloaded")

    # Validate that the search results page is displayed
    await expect(async_page).to_have_url(
        re.compile(r".*/s\?k=.*"),
        timeout=20000
    )

    # Step 4: Locate product cards
    product_cards = async_page.locator(
        "div[data-component-type='s-search-result']"
    )

    await expect(product_cards.first).to_be_visible(timeout=20000)

    product_count = await product_cards.count()

    print(f"\nTotal product cards found: {product_count}")

    # Step 5: Find a product with a visible title and product link
    selected_product = None

    for index in range(product_count):

        card = product_cards.nth(index)

        # Get the product title
        heading = card.locator("h2").first

        if not await heading.is_visible():
            continue

        title = (await heading.inner_text()).strip()

        if not title:
            continue

        # Find the product details link
        product_link = card.locator("a[href*='/dp/']").first

        if await product_link.count() == 0:
            continue

        if not await product_link.is_visible():
            continue

        product_url = await product_link.get_attribute("href")

        if not product_url:
            continue

        # Save the first suitable product
        selected_product = {
            "title": title,
            "link": product_link,
            "url": product_url
        }

        break

    # Step 6: Validate that a suitable product was found
    assert selected_product is not None, (
        "No suitable product with a visible title and product link was found."
    )

    print("\nSelected product title:", selected_product["title"])
    print("Selected product URL:", selected_product["url"])

    # Try to capture the displayed price if available
    selected_card = product_cards.filter(
        has=async_page.locator("h2").filter(
            has_text=selected_product["title"]
        )
    ).first

    price_locator = selected_card.locator(
        "span.a-price span.a-offscreen"
    ).first

    if await price_locator.count() > 0:
        price = (await price_locator.inner_text()).strip()
        print("Selected product price:", price)
    else:
        print("Product price is not available on the search results page.")

    # Step 7: Click the product and handle a new tab/window if one opens
    try:
        async with async_page.expect_popup(timeout=5000) as popup_info:
            await selected_product["link"].click()

        product_page = await popup_info.value

    except Exception:
        # If no new tab opens, continue on the current page
        product_page = async_page

    # Step 8: Wait for the product details page to load
    await product_page.wait_for_load_state("domcontentloaded")

    # Step 9: Validate the product details page title
    detail_title_locator = product_page.locator("#productTitle")

    await expect(detail_title_locator).to_be_visible(timeout=30000)

    detail_title = (await detail_title_locator.inner_text()).strip()

    print("\nProduct details title:", detail_title)
    print("Product details URL:", product_page.url)

    # Step 10: Verify that the product title is not empty
    assert detail_title, "Product details title is empty."

    # Step 11: Verify that the product details URL contains a product identifier
    assert "/dp/" in product_page.url, (
        f"Expected a product details URL, but got: {product_page.url}"
    )

    print("\nProduct discovery test completed successfully.")

