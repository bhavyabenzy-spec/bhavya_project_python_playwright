
from pathlib import Path

import pytest
from playwright.async_api import expect, TimeoutError


# Folder for the final product screenshot
SCREENSHOT_FOLDER = Path("artifacts/screenshots")


@pytest.mark.asyncio
async def test_amazon_end_to_end_shopping_journey(async_page):
    page = async_page

    # 1. Open Amazon India and verify the home page
 
    await page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    search_box = page.locator("#twotabsearchtextbox")
    await expect(search_box).to_be_visible(timeout=20000)

    print("\nStep 1: Amazon home page loaded successfully.")

    # 2. Hover over the account/sign-in menu
    
    account_menu = page.locator("#nav-link-accountList")
    account_flyout = page.locator("#nav-flyout-accountList")

    if await account_menu.is_visible():
        await account_menu.hover()

        try:
            await expect(account_flyout).to_be_visible(timeout=5000)
            print("Step 2: Account hover menu appeared.")
        except TimeoutError:
            print(
                "Step 2: Account hover menu was not available "
                "or did not appear."
            )
    else:
        print("Step 2: Account menu was unavailable.")

   
    # 3. Search using dynamic suggestions
    search_box = page.locator("#twotabsearchtextbox")
    await search_box.fill("Atomic Habits")

    suggestions = page.locator("div.s-suggestion")
    suggestion_selected = False

    try:
        # Wait for the first suggestion to appear
        await suggestions.first.wait_for(
            state="visible",
            timeout=5000
        )

        # Select the first visible suggestion with text
        for index in range(await suggestions.count()):
            suggestion = suggestions.nth(index)

            if await suggestion.is_visible():
                suggestion_text = (
                    await suggestion.inner_text()
                ).strip()

                if suggestion_text:
                    print(
                        f"Step 3: Selecting suggestion: "
                        f"{suggestion_text}"
                    )
                    await suggestion.click()
                    suggestion_selected = True
                    break

    except TimeoutError:
        print("Step 3: No autocomplete suggestions appeared.")

    # If suggestions are unavailable, submit the search normally
    if not suggestion_selected:
        await search_box.press("Enter")


    # 4. Verify search results
    results = page.locator(
        "div[data-component-type='s-search-result']"
    )

    await expect(results.first).to_be_visible(timeout=20000)
    initial_count = await results.count()

    assert initial_count > 0, "No Amazon search results found."

    print(
        f"Step 4: Search successful. "
        f"Products displayed: {initial_count}"
    )

  
    # 5. Scroll and check pagination/lazy-loaded content
    initial_height = await page.evaluate(
        "() => document.documentElement.scrollHeight"
    )

    for _ in range(4):
        await page.evaluate("window.scrollBy(0, 700)")

    # Check whether more products have appeared
    final_count = await results.count()

    # Check whether Amazon provides a next-page control
    next_page = page.locator("a.s-pagination-next")
    has_next_page = await next_page.is_visible()

    final_height = await page.evaluate(
        "() => document.documentElement.scrollHeight"
    )

    if final_count > initial_count:
        print("Step 5: Additional products appeared after scrolling.")
    elif has_next_page:
        print(
            "Step 5: Standard pagination is available; "
            "infinite scrolling was not confirmed."
        )
    else:
        print(
            "Step 5: Scrolling completed. "
            f"Initial height: {initial_height}, "
            f"final height: {final_height}. "
            "No increase in product count was confirmed."
        )


    # 6. Find Atomic Habits and open product details
  
    product_heading = page.get_by_text(
        "Atomic Habits",
        exact=False
    ).first

    await expect(product_heading).to_be_visible(timeout=15000)

    product_card = product_heading.locator(
        "xpath=ancestor::div[@data-component-type='s-search-result']"
    )

    await expect(product_card).to_be_visible()

    product_link = product_card.locator(
        "a[href*='/dp/']"
    ).first

    await expect(product_link).to_be_visible()

    # Amazon may open product details in a new tab
    async with page.expect_popup() as popup_info:
        await product_link.click()

    product_page = await popup_info.value

    await product_page.wait_for_load_state("domcontentloaded")

    # Verify the product title
    product_title = product_page.locator("#productTitle")
    await expect(product_title).to_be_visible(timeout=20000)

    actual_title = (
        await product_title.inner_text()
    ).strip()

    assert "Atomic Habits" in actual_title

    print(f"Step 6: Product title verified: {actual_title}")

    # Verify the product price
    price = product_page.locator(
        "span.a-price span.a-offscreen"
    ).first

    await expect(price).to_be_visible(timeout=15000)

    actual_price = (await price.inner_text()).strip()

    assert actual_price, "Product price is empty."

    print(f"Step 6: Product price verified: {actual_price}")

    # --------------------------------------------------
    # 7. Right-click a harmless element
    # --------------------------------------------------
    await product_title.click(button="right")

    # Playwright cannot inspect the operating system's
    # native context menu, so verify the page remains usable.
    await expect(product_title).to_be_visible()

    print(
        "Step 7: Right-click performed on the product title. "
        "Native context-menu contents were not verified."
    )


    # 8. Double-click harmless product title text
  
    await product_title.dblclick()

    await expect(product_title).to_be_visible()

    print("Step 8: Double-click performed on product title.")

   
    # 9. Check hidden account menu and reveal it normally
  
    product_account_menu = product_page.locator(
        "#nav-link-accountList"
    )

    product_account_flyout = product_page.locator(
        "#nav-flyout-accountList"
    )

    if (
        await product_account_menu.count() > 0
        and await product_account_menu.is_visible()
        and await product_account_flyout.count() > 0
    ):
        try:
            await expect(
                product_account_flyout
            ).to_be_hidden(timeout=5000)

            print("Step 9: Account flyout is initially hidden.")

            await product_account_menu.hover()

            await expect(
                product_account_flyout
            ).to_be_visible(timeout=5000)

            print(
                "Step 9: Account flyout became visible "
                "after normal hover."
            )

            # Move away to close the flyout normally
            await product_page.mouse.move(0, 0)

            await expect(
                product_account_flyout
            ).to_be_hidden(timeout=5000)

            print("Step 9: Account flyout is hidden again.")

        except TimeoutError:
            print(
                "Step 9: The account flyout visibility change "
                "could not be confirmed on this page."
            )
    else:
        print(
            "Step 9: No suitable account flyout was available "
            "for hidden-element verification."
        )

  
    # 10. Capture final screenshot of product details
    
    SCREENSHOT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    screenshot_path = (
        SCREENSHOT_FOLDER
        / "task1_amazon_product_details.png"
    )

    await product_page.screenshot(
        path=str(screenshot_path),
        full_page=True
    )

    print(f"Step 10: Screenshot saved at {screenshot_path}")

    # Close only the product tab opened by this test
    await product_page.close()
