
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_end_to_end_product_search_and_cart(async_page):

    # Step 1: Open Amazon India
    await async_page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    # Step 2: Search for books
    search_box = async_page.locator("#twotabsearchtextbox")
    await search_box.fill("books")
    await search_box.press("Enter")

    # Step 3: Locate product titles in search results
    titles = async_page.locator(
        'div[data-cy="title-recipe"] h2 span'
    )

    await expect(titles.first).to_be_visible(timeout=20000)

    # Step 4: Get the first product title
    product_title_text = (await titles.first.inner_text()).strip()
    print("Selected product:", product_title_text)

    # Step 5: Locate the link for the first product
    title_link = async_page.locator(
        'div[data-cy="title-recipe"] h2'
    ).first.locator("xpath=ancestor::a")

    await expect(title_link).to_be_visible(timeout=15000)

    # Step 6: Open the product page
    async with async_page.context.expect_page() as new_page_info:
        await title_link.click()

    product_page = await new_page_info.value
    await product_page.wait_for_load_state("domcontentloaded")

    # Step 7: Verify the product details page
    detail_title = product_page.locator("#productTitle")
    await expect(detail_title).to_be_visible(timeout=20000)

    actual_title = (await detail_title.inner_text()).strip()
    print("Product details:", actual_title)

    # Step 8: Check whether Add to Cart is available
    add_to_cart = product_page.locator("#add-to-cart-button")

    await expect(add_to_cart).to_be_visible(timeout=15000)
    await expect(add_to_cart).to_be_enabled(timeout=15000)

    # Step 9: Record the cart count before adding the product
    cart_count = product_page.locator("#nav-cart-count")

    before_text = (await cart_count.inner_text()).strip()
    before_count = int(before_text) if before_text.isdigit() else 0

    # Step 10: Add the product to the cart
    await add_to_cart.click()

    # Step 11: Verify the cart count changes
    await expect(cart_count).not_to_have_text(
        str(before_count),
        timeout=20000
    )

    after_text = (await cart_count.inner_text()).strip()
    print("Cart count before:", before_count)
    print("Cart count after:", after_text)

    # Step 12: Confirm the cart count increased
    assert after_text.isdigit(), "Cart count is not a number"
    assert int(after_text) > before_count, (
        "Cart count did not increase after adding the product"
    )

    print("End-to-end product search and cart validation passed.")

