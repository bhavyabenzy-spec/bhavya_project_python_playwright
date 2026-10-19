
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_robust_product_locator(async_page):

    # Step 1: Open Amazon India
    await async_page.goto("https://www.amazon.in/")

    # Step 2: Search for Atomic Habits
    search_box = async_page.locator("#twotabsearchtextbox")
    await search_box.fill("Atomic Habits")
    await search_box.press("Enter")

    # Step 3: Wait for search results
    await async_page.wait_for_load_state("domcontentloaded")

    # Step 4: Locate the product using its visible title
    target_product = "Atomic Habits: Tiny Changes, Remarkable Results"

    product_heading = async_page.get_by_text(
        target_product,
        exact=False
    ).first

    await expect(product_heading).to_be_visible(timeout=15000)

    # Step 5: Find the product card containing the matching title
    product_card = product_heading.locator(
        "xpath=ancestor::div[@data-component-type='s-search-result']"
    )

    await expect(product_card).to_be_visible()

    # Step 6: Verify that the correct product card was selected
    card_text = await product_card.inner_text()

    assert target_product.lower() in card_text.lower(), (
        "The selected product card does not contain the expected title."
    )

    print("\nCorrect product card selected:")
    print(card_text[:500])

    # Step 7: Find the product link inside the selected card
    product_link = product_card.locator(
        "a[href*='/dp/']"
    ).first

    await expect(product_link).to_be_visible()


    # Step 8: Click the product link and capture the new tab
    async with async_page.expect_popup() as popup_info:
        await product_link.click()

    # Get the newly opened tab
    product_page = await popup_info.value

    # Step 9: Verify the product details page in the new tab
    await product_page.wait_for_load_state("domcontentloaded")

    product_title = product_page.locator("#productTitle")

    await expect(product_title).to_be_visible(timeout=15000)

    actual_title = (await product_title.inner_text()).strip()

    assert "Atomic Habits" in actual_title, (
        f"Unexpected product page title: {actual_title}"
    )

    print("\nProduct page verified:", actual_title)



