
import pytest
from playwright.async_api import expect, TimeoutError


BASE_URL = "https://demowebshop.tricentis.com/"


@pytest.mark.asyncio
async def test_demowebshop_end_to_end_journey(async_page):
    page = async_page

    # 1. Open DemoWebShop
    await page.goto(BASE_URL, wait_until="domcontentloaded")

    # Verify that the main navigation is visible
    navigation = page.locator("ul.top-menu")
    await expect(navigation).to_be_visible(timeout=15000)

    print("Step 1: DemoWebShop home page loaded.")

    # 2. Hover over the Books category, if available
    books_link = navigation.locator("a[href*='/books']")

    if await books_link.count() > 0:
        await books_link.first.hover()
        print("Step 2: Hovered over the Books category.")
    else:
        print("Step 2: No suitable Books navigation link found.")

    # 3. Open the Books category
    if await books_link.count() > 0:
        await books_link.first.click()
        await expect(page.locator("h1")).to_be_visible(timeout=10000)
        print("Step 3: Books category opened.")
    else:
        # Fall back to the site's search feature
        print("Step 3: Using the site search instead.")

    # 4. Search for a book
    search_box = page.locator("#small-searchterms")
    await expect(search_box).to_be_visible()

    await search_box.fill("book")

    # Handle autocomplete suggestions if the site displays them
    suggestions = page.locator("ul.ui-autocomplete li")
    suggestion_selected = False

    try:
        await suggestions.first.wait_for(
            state="visible",
            timeout=3000
        )

        for index in range(await suggestions.count()):
            suggestion = suggestions.nth(index)

            if await suggestion.is_visible():
                suggestion_text = (
                    await suggestion.inner_text()
                ).strip()

                if suggestion_text:
                    await suggestion.click()
                    suggestion_selected = True
                    print(
                        f"Step 4: Selected suggestion: "
                        f"{suggestion_text}"
                    )
                    break

    except TimeoutError:
        print("Step 4: No autocomplete suggestions appeared.")

    if not suggestion_selected:
        await search_box.fill("book")
        await search_box.press("Enter")

    # 5. Verify product search results
    products = page.locator("div.product-item")
    await expect(products.first).to_be_visible(timeout=15000)

    initial_count = await products.count()
    assert initial_count > 0, "No products were returned."

    print(f"Step 5: Found {initial_count} products.")

    # Scroll incrementally through the listing
    for _ in range(3):
        await page.evaluate("window.scrollBy(0, 600)")

    final_count = await products.count()
    next_page = page.locator("a.next-page")

    if final_count > initial_count:
        print("Step 5: Additional products appeared after scrolling.")
    elif await next_page.count() > 0 and await next_page.is_visible():
        print("Step 5: Pagination is available.")
    else:
        print("Step 5: Scrolling completed; no additional products confirmed.")

    # 6. Open the first available product

    # Check the product price
    price = page.locator(".product-price").first

    # Verify that the price is visible
    await expect(price).to_be_visible(timeout=10000)

    # Read the displayed price
    actual_price = (await price.inner_text()).strip()

    # Verify that the price is not empty
    assert actual_price, "Product price is empty."

    print(f"Step 6: Product price verified: {actual_price}")


   
    # 7. Verify product details
    product_title = page.locator("div.product-name h1")

    # Check that the product title is visible
    await expect(product_title).to_be_visible()

    # Read and verify the product title
    actual_title = (await product_title.inner_text()).strip()

    assert actual_title, "Product title is empty."

    print(f"Step 7: Product details verified: {actual_title}")


    # 8. Right-click a harmless product title
    await product_title.click(button="right")
    await expect(product_title).to_be_visible()

    print("Step 7: Right-click completed.")

    # 9. Double-click the product title
    await product_title.dblclick()
    await expect(product_title).to_be_visible()

    print("Step 8: Double-click completed.")

    # 10. Check the cart notification before adding the product
    notification = page.locator("div.bar-notification")

    if await notification.count() > 0:
        if not await notification.is_visible():
            print("Step 9: Cart notification is initially hidden.")
        else:
            print("Step 9: Cart notification is already visible.")
    else:
        print("Step 9: No cart notification element was found initially.")

    # 11. Add the product to the cart
    add_to_cart_button = page.locator(
        "input.add-to-cart-button, button.add-to-cart-button"
    ).first

    await expect(add_to_cart_button).to_be_visible(timeout=10000)
    await expect(add_to_cart_button).to_be_enabled()

    await add_to_cart_button.click()

    # Verify the site's confirmation message
    await expect(notification).to_be_visible(timeout=10000)

    notification_text = (await notification.inner_text()).strip()
    print(f"Step 10: Cart confirmation: {notification_text}")

    # 12. Verify the cart count or cart contents
    cart_quantity = page.locator("span.cart-qty")
    await expect(cart_quantity).to_be_visible(timeout=10000)

    quantity_text = (await cart_quantity.inner_text()).strip()
    print(f"Step 11: Cart quantity displayed: {quantity_text}")

    # Stop here: do not proceed to checkout or place an order.
    print("Task 3 completed up to cart verification.")
