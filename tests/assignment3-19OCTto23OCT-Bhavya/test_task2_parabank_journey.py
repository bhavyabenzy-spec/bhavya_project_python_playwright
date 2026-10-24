
import os

import pytest
from dotenv import load_dotenv
from playwright.async_api import expect


load_dotenv()

BASE_URL = "https://parabank.parasoft.com/parabank/index.htm"


@pytest.mark.asyncio
async def test_parabank_end_to_end_journey(async_page):
    page = async_page

    # Read credentials from the local .env file
    username = os.getenv("PARABANK_USERNAME")
    password = os.getenv("PARABANK_PASSWORD")

    if not username or not password:
        pytest.skip(
            "Add PARABANK_USERNAME and PARABANK_PASSWORD to .env first."
        )

    # 1. Open ParaBank and log in
    await page.goto(BASE_URL, wait_until="domcontentloaded")

    await page.locator("input[name='username']").fill(username)
    await page.locator("input[name='password']").fill(password)
    await page.get_by_role("button", name="Log In").click()

    # 2. Verify the account overview
    await expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible(timeout=15000)

    print("Step 1: Logged in; account overview displayed.")

    # 3. Open account details through the navigation
    await page.get_by_role("link", name="Accounts Overview").click()

    account_links = page.locator(
        "table#accountTable a[href*='activity.htm?id=']"
    )
    await expect(account_links.first).to_be_visible(timeout=10000)

    first_account_id = (await account_links.first.inner_text()).strip()
    assert first_account_id
    print(f"Step 2: Account details link found: {first_account_id}")

    await account_links.first.click()
    await expect(
        page.get_by_role("heading", name="Account Details")
    ).to_be_visible(timeout=10000)

    # 4. Open a second account so a transfer has two accounts to use
    await page.get_by_role("link", name="Open New Account").click()

    account_type = page.locator("#type")
    await expect(account_type).to_be_visible(timeout=10000)

    # Select a supported account type from the site's dropdown
    options = await account_type.locator("option").all()
    available_types = []

    for option in options:
        value = await option.get_attribute("value")
        if value:
            available_types.append(value)

    if not available_types:
        pytest.fail("No account types were available in the dropdown.")

    await account_type.select_option(available_types[0])

    source_dropdown = page.locator("#fromAccountId")
    await expect(source_dropdown).to_be_visible()

    source_options = await source_dropdown.locator("option").all()
    source_values = []

    for option in source_options:
        value = await option.get_attribute("value")
        if value:
            source_values.append(value)

    if not source_values:
        pytest.fail("No source account was available.")

    await source_dropdown.select_option(source_values[0])

    await page.get_by_role("button", name="Open New Account").click()

    new_account_link = page.locator("#newAccountId")
    await expect(new_account_link).to_be_visible(timeout=15000)

    new_account_id = (await new_account_link.inner_text()).strip()
    print(f"Step 3: New demo account opened: {new_account_id}")

    # 5. Open the transfer-funds page
    await page.get_by_role("link", name="Transfer Funds").click()

    amount_input = page.locator("#amount")
    from_dropdown = page.locator("#fromAccountId")
    to_dropdown = page.locator("#toAccountId")

    await expect(amount_input).to_be_visible()
    await expect(from_dropdown).to_be_visible()
    await expect(to_dropdown).to_be_visible()

    from_values = []
    for option in await from_dropdown.locator("option").all():
        value = await option.get_attribute("value")
        if value:
            from_values.append(value)

    to_values = []
    for option in await to_dropdown.locator("option").all():
        value = await option.get_attribute("value")
        if value:
            to_values.append(value)

    # Find two different account IDs
    pair = None

    for source in from_values:
        for destination in to_values:
            if source != destination:
                pair = (source, destination)
                break
        if pair:
            break

    if not pair:
        pytest.fail(
            "Two different accounts are required for a transfer."
        )

    source_id, destination_id = pair

    # 6. Submit a small demo transfer
    # This affects only the public demo site's test account.
    await from_dropdown.select_option(source_id)
    await to_dropdown.select_option(destination_id)
    await amount_input.fill("1")

    await page.get_by_role("button", name="Transfer").click()

    transfer_result = page.get_by_text(
        "Transfer Complete!",
        exact=False
    )
    await expect(transfer_result).to_be_visible(timeout=15000)

    print(
        f"Step 4: Transfer result displayed: "
        f"{source_id} -> {destination_id}"
    )

    # 7. Check the account overview after the transfer
    await page.get_by_role("link", name="Accounts Overview").click()

    await expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible(timeout=10000)

    print("Step 5: Returned to account overview.")

    # 8. Hover if a suitable navigation item is available
    nav_link = page.get_by_role("link", name="Accounts Overview")

    if await nav_link.is_visible():
        await nav_link.hover()
        print("Step 6: Hovered over the navigation link.")
    else:
        print("Step 6: No suitable navigation link was visible.")

    # 9. Log out and verify the signed-out page
    await page.get_by_role("link", name="Log Out").click()

    await expect(
        page.locator("input[name='username']")
    ).to_be_visible(timeout=10000)

    print("Step 7: Logged out successfully.")
