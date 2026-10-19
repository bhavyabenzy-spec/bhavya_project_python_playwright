
import pytest
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


@pytest.mark.asyncio
async def test_timeout_handling(async_page):

    # Step 1: Set the default timeout to 5 seconds
    # Playwright will use this timeout for actions by default.
    async_page.set_default_timeout(5000)

    # Step 2: Open Amazon India
    await async_page.goto(
        "https://www.amazon.in/",
        wait_until="domcontentloaded"
    )

    print("Amazon India opened successfully.")

    # Step 3: Wait for a valid element using a custom timeout
    # The search box should appear within 10 seconds.
    search_box = async_page.locator("#twotabsearchtextbox")

    await search_box.wait_for(
        state="visible",
        timeout=10000
    )

    print("Search box is visible. Custom wait successful.")

    # Step 4: Try waiting for an element that does not exist
    # This locator is intentionally incorrect for this test.
    missing_element = async_page.locator(
        "#this-element-does-not-exist"
    )

    try:
        await missing_element.wait_for(
            state="visible",
            timeout=3000
        )

        # This line runs only if the element unexpectedly appears.
        print("Unexpectedly, the missing element was found.")

    except PlaywrightTimeoutError:
        # Handle the expected timeout without failing the test.
        print(
            "Timeout occurred: The expected element was not found "
            "within 3 seconds."
        )

    print("Test completed successfully.")
