
import os
import pytest
from dotenv import load_dotenv
from playwright.async_api import expect

# Load username and password from the .env file
load_dotenv()


@pytest.mark.asyncio
async def test_parabank_end_to_end_journey(async_page):
    page = async_page

    # --------------------------------------------------
    # STEP 1: Open ParaBank and log in
    # --------------------------------------------------
    await page.goto("https://parabank.parasoft.com/parabank/index.htm")

    username = os.getenv("PARABANK_USERNAME")
    password = os.getenv("PARABANK_PASSWORD")

    # Make sure the credentials are available in .env
    assert username, "PARABANK_USERNAME is missing from the .env file"
    assert password, "PARABANK_PASSWORD is missing from the .env file"

    # Enter login credentials
    await page.locator('input[name="username"]').fill(username)
    await page.locator('input[name="password"]').fill(password)

    # Click Log In
    await page.get_by_role("button", name="Log In").click()

    # Verify successful login
    await expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible(timeout=15000)

    print("Step 1: Login successful.")

    # --------------------------------------------------
    # STEP 2: Verify the accounts overview
    # --------------------------------------------------
    account_rows = page.locator("#accountTable tbody tr")

    await expect(account_rows.first).to_be_visible(timeout=10000)

    row_count = await account_rows.count()
    assert row_count > 0, "No bank accounts were displayed."

    print(f"Step 2: Accounts Overview verified. Rows found: {row_count}")

    # --------------------------------------------------
    # STEP 3: Open the first account and verify details
    # --------------------------------------------------
    account_link = page.locator("#accountTable tbody tr td a").first

    await expect(account_link).to_be_visible()

    original_account_number = (await account_link.inner_text()).strip()

    await account_link.click()

    # Verify the Account Details page
    await expect(
        page.get_by_role("heading", name="Account Details")
    ).to_be_visible(timeout=10000)

    print(
        f"Step 3: Account details verified for account "
        f"{original_account_number}."
    )

    # Return to Accounts Overview
    await page.get_by_role(
        "link", name="Accounts Overview"
    ).click()

    await expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible()

    # --------------------------------------------------
    # STEP 4: Open a new bank account
    # --------------------------------------------------
    await page.get_by_role(
        "link", name="Open New Account"
    ).click()

    await expect(
        page.get_by_role("heading", name="Open New Account")
    ).to_be_visible(timeout=10000)

    # Select the account type
    account_type = page.locator("#type")

    await expect(account_type).to_be_visible()
    await account_type.select_option(label="CHECKING")

    # Find the existing account dropdown
    funding_dropdown = page.locator("#fromAccountId")

    await expect(funding_dropdown).to_be_visible(timeout=10000)

    # Wait until at least one option is available
    await expect(
        funding_dropdown.locator("option").first
    ).to_be_attached(timeout=15000)

    # Read the available funding accounts
    funding_options = await funding_dropdown.locator("option").all()

    funding_account = None

    for option in funding_options:
        value = await option.get_attribute("value")
        account_text = (await option.inner_text()).strip()

        print(
            f"Available funding account: {account_text}, "
            f"value={value!r}"
        )

        # Select the first option with a valid account value
        if value and value.strip():
            funding_account = value
            break

    assert funding_account is not None, (
        "No existing funding account was available."
    )

    await funding_dropdown.select_option(value=funding_account)

    # Submit the new account request
    await page.get_by_role(
        "button", name="Open New Account"
    ).click()

    # Verify that the new account number is displayed
    new_account_number = page.locator("#newAccountId")

    await expect(
        new_account_number
    ).to_be_visible(timeout=15000)

    new_account_id = (await new_account_number.inner_text()).strip()

    assert new_account_id, "The new account number was not displayed."

    print(
        f"Step 4: New account opened successfully. "
        f"Account number: {new_account_id}"
    )

    # --------------------------------------------------
    # STEP 5: Transfer funds between accounts
    # --------------------------------------------------
    await page.get_by_role(
        "link", name="Transfer Funds"
    ).click()

    await expect(
        page.get_by_role("heading", name="Transfer Funds")
    ).to_be_visible(timeout=10000)

    # Wait for the source and destination dropdowns
    from_dropdown = page.locator("#fromAccountId")
    to_dropdown = page.locator("#toAccountId")

    await expect(from_dropdown).to_be_visible()
    await expect(to_dropdown).to_be_visible()

    # Wait until the source dropdown has at least one option
    await expect(
        from_dropdown.locator("option").first
    ).to_be_attached(timeout=10000)

    # Print all source account options for debugging
    from_options = await from_dropdown.locator("option").all()

    print("\nSource account dropdown options:")

    available_accounts = []

    for option in from_options:
        value = await option.get_attribute("value")
        text_value = (await option.inner_text()).strip()

        print(f"Text: {text_value!r}, Value: {value!r}")

        if value and value.strip():
            available_accounts.append(value)

    # Print all destination account options
    to_options = await to_dropdown.locator("option").all()

    print("\nDestination account dropdown options:")

    for option in to_options:
        value = await option.get_attribute("value")
        text_value = (await option.inner_text()).strip()

        print(f"Text: {text_value!r}, Value: {value!r}")

    # Stop with a clear message if the accounts are unavailable
    assert len(available_accounts) >= 2, (
        "Fewer than two source accounts were found. "
        "Check the printed dropdown options and confirm "
        "that the new account was created successfully."
    )

    # Select two different accounts
    source_account = available_accounts[0]
    destination_account = available_accounts[1]

    # Enter a $1 transfer
    await page.locator("#amount").fill("1")
    await from_dropdown.select_option(value=source_account)
    await to_dropdown.select_option(value=destination_account)

    # Submit the transfer
    await page.get_by_role(
        "button", name="Transfer"
    ).click()

    # Verify the result
    await expect(
        page.get_by_role("heading", name="Transfer Complete!")
    ).to_be_visible(timeout=15000)

    print(
        f"Step 5: Transfer completed successfully. "
        f"From: {source_account}, To: {destination_account}"
    )


    # --------------------------------------------------
    # STEP 6: Return to Accounts Overview
    # --------------------------------------------------
    await page.get_by_role(
        "link", name="Accounts Overview"
    ).click()

    await expect(
        page.get_by_role("heading", name="Accounts Overview")
    ).to_be_visible(timeout=10000)

    print("Step 6: Returned to Accounts Overview successfully.")

    # --------------------------------------------------
    # STEP 7: Verify and hover over About Us
    # --------------------------------------------------
    # IMPORTANT:
    # About Us appears in both the header and footer.
    # Use #headerPanel to select only the header link.
    about_us_link = page.locator(
        "#headerPanel"
    ).get_by_role("link", name="About Us")

    await expect(about_us_link).to_be_visible()
    await about_us_link.hover()

    print("Step 7: About Us header link verified successfully.")

    # --------------------------------------------------
    # STEP 8: Log out
    # --------------------------------------------------
    await page.get_by_role("link", name="Log Out").click()

    # Verify that the Customer Login section appears again
    await expect(
        page.get_by_role("heading", name="Customer Login")
    ).to_be_visible(timeout=10000)

    print("Step 8: Logout successful.")

    print("ParaBank end-to-end journey completed successfully.")
