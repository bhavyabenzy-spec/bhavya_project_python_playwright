
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_task7_locators_and_debugging(async_page, base_url):
    page = async_page

    # STEP 1: Open the website
    await page.goto(base_url)

    # STEP 2: Locate an element by its role and accessible name
    logo = page.get_by_role(
        "link",
        name="Tricentis Demo Web Shop"
    )
    await expect(logo).to_be_visible()

    # STEP 3: Locate the search box using its placeholder
    search_box = page.get_by_placeholder("Search store")
    await expect(search_box).to_be_visible()

    # STEP 4: Locate the search button by its role
    search_button = page.get_by_role(
        "button",
        name="Search"
    )
    await expect(search_button).to_be_visible()

    # STEP 5: Search for a product
    await search_box.fill("computer")
    await search_button.click()

    # STEP 6: Locate a result using visible text
    await expect(
        page.get_by_text("computer", exact=False).first
    ).to_be_visible()

    # STEP 7: Filter product result containers by text
    product_results = page.locator(
        "div.product-item"
    ).filter(has_text="computer")

    # Print the number of matching products
    print(
        "Matching products:",
        await product_results.count()
    )

    # STEP 8: Pause here when debugging in headed mode
    # Uncomment the next line when you want to inspect the page.
    # await page.pause()
