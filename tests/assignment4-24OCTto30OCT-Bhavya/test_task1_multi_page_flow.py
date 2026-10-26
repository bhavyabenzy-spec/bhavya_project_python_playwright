
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_product_search_add_to_cart_and_verify(async_page):
    page = async_page

    # STEP 1: Open the Demo Web Shop home page
    await page.goto("https://demowebshop.tricentis.com/")

    await expect(
        page.get_by_role("link", name="Tricentis Demo Web Shop")
    ).to_be_visible()

    print("Step 1: Demo Web Shop home page opened.")

    
    # STEP 2: Search for Simple Computer
    search_box = page.locator("#small-searchterms")

    # Verify the search box is available
    await expect(search_box).to_be_visible(timeout=15000)

    # Enter the product name and search
    await search_box.fill("Simple Computer")
    await page.locator("input.button-1.search-box-button").click()

    print("Step 2: Searched for Simple Computer.")

    
    # STEP 3: Open the product details page

    # Find the Simple Computer link in the search results
    product_link = page.get_by_role("link", name="Simple Computer", exact=True)

    # Verify the product link is visible
    await expect(product_link).to_be_visible(timeout=15000)

    # Click the product to open its details page
    await product_link.click()

    # Verify that the product details page has opened
    product_title = page.locator("div.product-name h1")
    await expect(product_title).to_be_visible(timeout=15000)

    # Capture the product name
    product_name = (await product_title.inner_text()).strip()

    # Capture the displayed product price
    price_locator = page.locator(".product-price").first
    await expect(price_locator).to_be_visible()

    product_price = (await price_locator.inner_text()).strip()

    # Confirm the product details are available
    assert product_name, "Product name is empty."
    assert product_price, "Product price is empty."

    # Store the name and price for verification in the cart
    selected_product = {
        "name": product_name,
        "price": product_price
    }

    print(f"Step 3: Product details verified: {selected_product}")


    # STEP 4: Add the product to the cart
    # Find Add to cart inside the product details form
    add_to_cart_button = page.locator("#product-details-form").get_by_role(
        "button", name="Add to cart"
    )

    await expect(add_to_cart_button).to_be_visible()
    await add_to_cart_button.click()

    # Wait for the website's confirmation message
    success_message = page.locator(".bar-notification.success")

    await expect(success_message).to_be_visible(timeout=10000)

    print("Step 4: Product added to the cart.")

    # STEP 5: Open the shopping cart
    await page.get_by_role(
        "link", name="Shopping cart"
    ).click()

    await expect(
        page.get_by_role("heading", name="Shopping cart")
    ).to_be_visible(timeout=15000)

    # STEP 6: Verify the selected product appears in the cart
    cart_product = page.locator(
        "table.cart tbody tr"
    ).filter(has_text=selected_product["name"])

    await expect(cart_product).to_be_visible(timeout=10000)

    # Verify the product name is present
    await expect(cart_product).to_contain_text(
        selected_product["name"]
    )

    # Verify the price matches the product page
    cart_price = cart_product.locator(".product-unit-price")

    await expect(cart_price).to_be_visible()

    actual_cart_price = (await cart_price.inner_text()).strip()

    assert actual_cart_price == selected_product["price"], (
        f"Price mismatch. Product page: {selected_product['price']}, "
        f"Cart page: {actual_cart_price}"
    )

    # Verify quantity is at least one
    quantity = cart_product.locator("input.qty-input")
    await expect(quantity).to_have_value("1")

    print(
        f"Step 6: Cart verified. Product: {selected_product['name']}, "
        f"Price: {actual_cart_price}, Quantity: 1"
    )

    print("Task 1: Multi-page product flow completed successfully.")
