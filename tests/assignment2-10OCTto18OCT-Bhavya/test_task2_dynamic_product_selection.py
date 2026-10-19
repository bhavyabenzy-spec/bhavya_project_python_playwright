import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_dynamic_product_selection(async_page):

    # Step 1: Open Amazon India
    await async_page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    # Step 2: Search for books
    search_box = async_page.locator("#twotabsearchtextbox")

    await expect(search_box).to_be_visible(timeout=15000)

    await search_box.fill("Book")
    await search_box.press("Enter")

    # Step 3: Wait until the search results are displayed
    product_cards = async_page.locator(
        "div[data-component-type='s-search-result']"
    )

    await expect(product_cards.first).to_be_visible(timeout=20000)

    print("\nSearching for a product with 'Book' in its title...")

    # Step 4: Define the keyword we want to find
    required_keyword = "book"

    # Initially, no product has been selected
    matched_title = None
    matched_link = None

    # Step 5: Check each product card until a matching title is found
    total_products = await product_cards.count()

    for index in range(total_products):

        # Get one product card
        card = product_cards.nth(index)

        # Find the title inside this card
        title_locator = card.locator("h2").first

        if not await title_locator.is_visible():
            continue

        title = (await title_locator.inner_text()).strip()

        # Check whether the title contains our keyword
        if required_keyword.lower() in title.lower():

            # Find the product link inside the SAME card
            product_link = card.locator("a[href*='/dp/']").first

            if await product_link.count() > 0:
                if await product_link.is_visible():

                    matched_title = title
                    matched_link = product_link

                    print("\nMatching product found!")
                    print("Product title:", matched_title)

                    # Stop after finding the first suitable match
                    break

    # Step 6: Fail clearly if no matching product was found
    assert matched_title is not None, (
        f"No product found with '{required_keyword}' in its title."
    )

    assert matched_link is not None, (
        "The matching product does not have a visible product link."
    )

    # Step 7: Click the link belonging to the matching product
    try:
        async with async_page.expect_popup(timeout=5000) as popup_info:
            await matched_link.click()

        product_page = await popup_info.value

    except Exception:
        # Use the current page if the product opens in the same tab
        product_page = async_page

    # Step 8: Validate the product details page
    detail_title = product_page.locator("#productTitle")

    await expect(detail_title).to_be_visible(timeout=30000)

    actual_title = (await detail_title.inner_text()).strip()

    print("\nProduct details page opened.")
    print("Details title:", actual_title)
    print("Product URL:", product_page.url)

    # Step 9: Check that the details page has a valid title
    assert actual_title, "The product details title is empty."

    assert "/dp/" in product_page.url, (
        "The opened page is not a product details page."
    )

    print("\nTask 2 completed successfully!")
