
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_static_dropdown(async_page):

    # Step 1: Open the practice page
    await async_page.goto(
        "https://www.playwrightautomation.com/practice.html",
        wait_until="domcontentloaded"
    )

    # Step 2: Find the native dropdown in the Static Dropdowns section
    # We use the label to locate the correct dropdown.
    country_dropdown = async_page.get_by_label(
        "Select Country"
    )

    # Step 3: Check that the dropdown is visible
    await expect(country_dropdown).to_be_visible(
        timeout=10000
    )

    # Step 4: Print the available options
    options = await country_dropdown.locator(
        "option"
    ).all_text_contents()

    print("Available countries:", options)

    # Step 5: Select India by its visible label
    # This assumes India is one of the available options.
    await country_dropdown.select_option(label="India")

    # Step 6: Validate the selected option
    selected_value = await country_dropdown.input_value()

    selected_label = await country_dropdown.locator(
        "option:checked"
    ).inner_text()

    print("Selected country:", selected_label)
    print("Selected value:", selected_value)

    # Step 7: Confirm that the selected option is India
    assert selected_label.strip() == "India", (
        f"Expected India, but selected {selected_label!r}"
    )

    print("Static dropdown test completed successfully.")
