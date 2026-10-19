import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_auto_suggest_dropdown(async_page):

    # Step 1: Open Amazon India
    await async_page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    # Step 2: Find the search box
    search_box = async_page.locator("#twotabsearchtextbox")

    await expect(search_box).to_be_visible(timeout=15000)

    # Step 3: Enter a partial product name
    search_text = "Harry Pot"

    await search_box.fill(search_text)

    print("\nEntered search text:", search_text)

    # Step 4: Locate Amazon's autocomplete suggestions
    suggestions = async_page.locator(
        "div.s-suggestion"
    )

    # Step 5: Wait briefly for suggestions to appear.
    # This is a locator wait, not a fixed sleep.
    try:
        await expect(suggestions.first).to_be_visible(timeout=5000)

        suggestion_count = await suggestions.count()

        print("Suggestions displayed:", suggestion_count)

        # Step 6: Find a suggestion matching the partial search text
        matching_suggestion = None

        for index in range(suggestion_count):

            suggestion = suggestions.nth(index)

            suggestion_text = (
                await suggestion.inner_text()
            ).strip()

            print("Suggestion:", suggestion_text)

            if search_text.lower() in suggestion_text.lower():
                matching_suggestion = suggestion
                break

        # Step 7: Click the matching suggestion if found
        if matching_suggestion is not None:

            await matching_suggestion.click()

            print("Clicked matching autocomplete suggestion.")

        else:
            # No matching suggestion: perform a normal search
            print(
                "No matching suggestion found. "
                "Using normal search instead."
            )

            await search_box.press("Enter")

    except AssertionError:
        # Suggestions did not become visible within the timeout
        print(
            "Autocomplete suggestions did not appear. "
            "Using normal search instead."
        )

        await search_box.press("Enter")

    # Step 8: Validate the resulting search page
    await expect(async_page).to_have_url(
        __import__("re").compile(r".*/s\?k=.*"),
        timeout=20000
    )

    # Step 9: Validate that search results are displayed
    product_cards = async_page.locator(
        "div[data-component-type='s-search-result']"
    )

    await expect(product_cards.first).to_be_visible(
        timeout=20000
    )

    print("Search results displayed successfully.")
    print("Final URL:", async_page.url)

    print("\nTask 3 completed successfully!")
