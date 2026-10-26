
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_conditional_ui_empty_and_nonempty_cart(async_page):
    page = async_page

    # STEP 1: Open Demo Web Shop
    await page.goto("https://demowebshop.tricentis.com/")

    print("Step 1: Demo Web Shop opened.")

    # STEP 2: Open the shopping cart
    await page.get_by_role("link", name="Shopping cart").click()

    # Verify that the shopping cart page opened
    await expect(
        page.get_by_role("heading", name="Shopping cart")
    ).to_be_visible()

    print("Step 2: Shopping cart opened.")

    # STEP 3: Check whether the cart is empty or contains products
    cart_rows = page.locator("table.cart tbody tr")
    row_count = await cart_rows.count()

    if row_count == 0:
        # Handle the empty-cart condition
        print("Condition: Shopping cart is empty.")

        # Verify the empty-cart message
        await expect(
            page.locator(".order-summary-content")
        ).to_contain_text("Your Shopping Cart is empty")

    else:
        # Handle the non-empty-cart condition
        print("Condition: Shopping cart contains products.")

        # Verify that at least one cart row is visible
        await expect(cart_rows.first).to_be_visible()

    # STEP 4: Return to the home page
    await page.goto("https://demowebshop.tricentis.com/")

    # STEP 5: Search for Simple Computer
    search_box = page.locator("#small-searchterms")
    await expect(search_box).to_be_visible()

    await search_box.fill("Simple Computer")
    await page.locator("input.button-1.search-box-button").click()

    # Verify that the product appears in search results
    product_link = page.get_by_role(
        "link",
        name="Simple Computer",
        exact=True
    )
    await expect(product_link).to_be_visible()

    # STEP 6: Open the product details page
    await product_link.click()

    # STEP 7: Check the Add to cart button before clicking
    add_to_cart_button = page.locator("#product-details-form").get_by_role(
        "button",
        name="Add to cart"
    )

    # Verify that the button is visible
    await expect(add_to_cart_button).to_be_visible()

    # Verify that the button is enabled
    await expect(add_to_cart_button).to_be_enabled()

    # Click only after both checks pass
    await add_to_cart_button.click()

    print("Step 7: Product added to cart.")

    # STEP 8: Verify the success notification
    success_message = page.locator(".bar-notification.success")
    await expect(success_message).to_be_visible(timeout=10000)

    # STEP 9: Open the shopping cart again
    await page.get_by_role("link", name="Shopping cart").click()

    await expect(
        page.get_by_role("heading", name="Shopping cart")
    ).to_be_visible()

    # STEP 10: Verify that the cart now contains a product
    cart_rows = page.locator("table.cart tbody tr")
    await expect(cart_rows.first).to_be_visible()

    await expect(cart_rows.first).to_contain_text("Simple Computer")

    print("Step 10: Non-empty cart verified.")
