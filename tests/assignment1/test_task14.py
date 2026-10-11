import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_multiple_locators():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Open SauceDemo
        await page.goto("https://www.saucedemo.com/")

        # Login
        await page.locator('[data-test="username"]').fill("standard_user")
        await page.locator('[data-test="password"]').fill("secret_sauce")
        await page.locator('[data-test="login-button"]').click()

        # 1. Find all matching product names
        products = page.locator(".inventory_item_name")

        # 2. Print the count
        count = await products.count()
        print("Total products:", count)

        # 3. Interact with the first matching element
        first_product = products.first
        print("First product:", await first_product.inner_text())

        await first_product.click()
        await expect(page).to_have_url(
            "https://www.saucedemo.com/inventory-item.html?id=4"
        )
        await page.go_back()

        # 4. Interact with the last matching element
        last_product = products.last
        print("Last product:", await last_product.inner_text())

        await last_product.click()
        await expect(page).to_have_url(
            "https://www.saucedemo.com/inventory-item.html?id=3"
        )
        await page.go_back()


        # 5. Interact with a specific element using nth()
        third_product = products.nth(2)

        print("Third product:", await third_product.inner_text())

        await third_product.click()

        await expect(page).to_have_url(
            "https://www.saucedemo.com/inventory-item.html?id=1"
        )
        await page.go_back()

        # 6. Loop through all matching elements and print text
        product_names = await products.all_text_contents()

        print("All product names:")

        for name in product_names:
            print(name)

        # 7. Verify expected number of products
        await expect(products).to_have_count(6)

        print("Product count verification passed!")

        await browser.close()