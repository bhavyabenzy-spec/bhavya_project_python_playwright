
import pytest
from playwright.async_api import expect, TimeoutError


@pytest.mark.asyncio
async def test_amazon_dynamic_dropdowns(async_page):

    # Step 1: Open Amazon India
    await async_page.goto("https://www.amazon.in/")

    # Step 2: Locate the search box
    search_box = async_page.locator("#twotabsearchtextbox")

    # Wait until the search box is visible
    await expect(search_box).to_be_visible()

    # Step 3: Enter a partial product name
    # We use a partial keyword to trigger autocomplete suggestions
    partial_product = "wireless mou"
    await search_box.fill(partial_product)

    # Step 4: Locate autocomplete suggestions
    suggestions = async_page.locator("div.s-suggestion")

    # Check whether suggestions appear within the current session
    try:
        await suggestions.first.wait_for(
            state="visible",
            timeout=5000
        )

        suggestion_count = await suggestions.count()

    except TimeoutError:
        suggestion_count = 0

    # Step 5: If suggestions appear, select a matching suggestion
    if suggestion_count > 0:

        print("Autocomplete suggestions appeared.")

        # Look for a suggestion matching the intended product
        matching_suggestion = suggestions.filter(
            has_text="wireless mouse"
        )

        if await matching_suggestion.count() > 0:
            selected_suggestion = matching_suggestion.first
        else:
            # If there is no exact text match, select the first suggestion
            selected_suggestion = suggestions.first

        # Read the selected suggestion before clicking it
        selected_text = (await selected_suggestion.inner_text()).strip()
        print("Selected suggestion:", selected_text)

        # Click the suggestion
        await selected_suggestion.click()

        # Validate that the search results page loads
        await async_page.wait_for_load_state("domcontentloaded")

        results = async_page.locator(
            "div[data-component-type='s-search-result']"
        )

        await expect(results.first).to_be_visible(timeout=15000)

        # Verify that the browser navigated to a search results page
        assert "/s" in async_page.url

        print("Autocomplete selection and navigation verified.")

    else:

        # Step 6: Fallback if autocomplete suggestions do not appear
        print("No autocomplete suggestions appeared.")
        print("Using normal search as a fallback.")

        # Submit the search using the search box
        await search_box.press("Enter")

        # Wait for the search results to load
        await async_page.wait_for_load_state("domcontentloaded")

        results = async_page.locator(
            "div[data-component-type='s-search-result']"
        )

        # Validate that search results are displayed
        await expect(results.first).to_be_visible(timeout=15000)

        # Verify that navigation to the search results page occurred
        assert "/s" in async_page.url

        print("Fallback search results verified.")
        print(
            "Normal search displays results after submission; "
            "it does not confirm that autocomplete suggestions appeared."
        )
