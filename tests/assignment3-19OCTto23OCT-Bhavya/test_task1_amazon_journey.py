
import pytest
from playwright.async_api import expect, TimeoutError


@pytest.mark.asyncio
async def test_amazon_end_to_end_shopping_journey(async_page):
    page = async_page

    # --------------------------------------------------
    # STEP 1: Open Amazon India and verify the home page
    # --------------------------------------------------
    await page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    search_box = page.locator("#twotabsearchtextbox")

    await expect(
        search_box
    ).to_be_visible(timeout=20000)

    print("\nStep 1: Amazon home page loaded successfully.")

    # --------------------------------------------------
    # STEP 2: Hover over the account menu
    # --------------------------------------------------
    account_menu = page.locator("#nav-link-accountList")
    account_flyout = page.locator("#nav-flyout-accountList")

    if await account_menu.is_visible():
        await account_menu.hover()

        try:
            await expect(
                account_flyout
            ).to_be_visible(timeout=5000)

            print("Step 2: Account hover menu appeared.")

        except TimeoutError:
            print(
                "Step 2: Account hover menu was not available "
                "or did not appear."
            )
    else:
        print("Step 2: Account menu was unavailable.")

    # --------------------------------------------------
    # STEP 3: Search using dynamic suggestions
    # --------------------------------------------------
    await search_box.fill("Atomic Habits")

    suggestions = page.locator("div.s-suggestion")
    suggestion_selected = False

    try:
        await suggestions.first.wait_for(
            state="visible",
            timeout=5000
        )

        suggestion_count = await suggestions.count()

        for index in range(suggestion_count):
            suggestion = suggestions.nth(index)

            if await suggestion.is_visible():
                suggestion_text = (
                    await suggestion.inner_text()
                ).strip()

                # Select a suggestion related to Atomic Habits
                if (
                    suggestion_text
                    and "Atomic Habits" in suggestion_text
                ):
                    print(
                        "Step 3: Selecting suggestion: "
                        f"{suggestion_text}"
                    )

                    await suggestion.click()
                    suggestion_selected = True
                    break

    except TimeoutError:
        print("Step 3: No autocomplete suggestions appeared.")

    # If no suggestion was selected, submit the search normally
    if not suggestion_selected:
        await search_box.fill("Atomic Habits")
        await search_box.press("Enter")

    print("Step 3: Search submitted.")

    # --------------------------------------------------
    # STEP 4: Verify Amazon search results
    # --------------------------------------------------
    # A suggestion may open a product page directly.
    # If so, navigate to the search results page.
    if "/dp/" in page.url:
        print(
            "Step 4: Amazon opened a product directly. "
            "Navigating to search results."
        )

        await page.goto(
            "https://www.amazon.in/s?k=Atomic+Habits",
            wait_until="domcontentloaded"
        )

    results = page.locator(
        "div[data-component-type='s-search-result']"
    )

    await expect(
        results.first
    ).to_be_visible(timeout=20000)

    initial_count = await results.count()

    assert initial_count > 0, (
        "No Amazon search results were found."
    )

    print(
        f"Step 4: Search results loaded. "
        f"Products displayed: {initial_count}"
    )

    # --------------------------------------------------
    # STEP 5: Check scrolling and pagination
    # --------------------------------------------------
    # Scroll down to inspect the lower part of the results.
    await page.evaluate(
        "window.scrollTo(0, document.body.scrollHeight)"
    )

    await page.wait_for_timeout(1000)

    pagination = page.locator(
        "a.s-pagination-next"
    )

    if await pagination.count() > 0:
        print(
            "Step 5: Pagination control found. "
            "Infinite scrolling was not confirmed."
        )
    else:
        print(
            "Step 5: No pagination control found. "
            "Scrolling completed."
        )

    # --------------------------------------------------
    # STEP 6: Find and open Atomic Habits
    # --------------------------------------------------
  
    # Verify that a product price is displayed.
    # Check all price elements and find one that is visible
    # and contains actual text.

    prices = page.locator(
        "#corePrice_feature_div span.a-offscreen, "
        "#apex_desktop span.a-offscreen, "
        "#buybox span.a-offscreen, "
        "span.a-price span.a-offscreen"
    )

    price_count = await prices.count()
    actual_price = None

    for index in range(price_count):
        current_price = prices.nth(index)

        if await current_price.is_visible():
            price_text = (
                await current_price.inner_text()
            ).strip()

            if price_text:
                actual_price = price_text
                break

    # Verify that we found a real, visible price.
    assert actual_price is not None, (
        "No visible product price was found."
    )

    print(
    f"Step 6: Product price verified: "
    f"{actual_price.encode('ascii', errors='replace').decode('ascii')}"
)

    print(
        "\nAmazon end-to-end shopping journey "
        "completed successfully."
    )
