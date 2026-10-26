
import pytest
from playwright.async_api import expect


# Test 1: Verify required-field validation
@pytest.mark.asyncio
async def test_form_required_field_validation(async_page):
    page = async_page

    # STEP 1: Open the multi-step form
    await page.goto(
        "https://lab.hakdogan.com/practice/form-multi-step/"
    )

    # Wait until the form is available
    form = page.locator('[data-testid="form-multi-step-form"]')
    await expect(form).to_be_visible()

    print("Step 1: Multi-step form opened.")

    # STEP 2: Click Next without entering any details
    next_button = page.locator(
        '[data-testid="form-multi-step-next"]'
    )
    await next_button.click()

    # STEP 3: Verify the required-field validation message
    validation_message = page.locator(
        '[data-testid="form-multi-step-result"]'
    )

    await expect(validation_message).to_contain_text(
        "First Name is required",
        ignore_case=True
    )

    print("Step 2: Required-field validation verified.")


# Test 2: Verify data persists when moving back
@pytest.mark.asyncio
async def test_form_data_persistence(async_page):
    page = async_page

    # STEP 1: Open the multi-step form
    await page.goto(
        "https://lab.hakdogan.com/practice/form-multi-step/"
    )

    form = page.locator('[data-testid="form-multi-step-form"]')
    await expect(form).to_be_visible()

    print("Step 1: Multi-step form opened.")

    # STEP 2: Enter personal details
    first_name = page.get_by_label("First Name")
    email = page.get_by_label("Email")

    await first_name.fill("Bhavya")
    await email.fill("bhavya.test@example.com")

    print("Step 2: Personal details entered.")

    # STEP 3: Move to the next step
    next_button = page.locator(
        '[data-testid="form-multi-step-next"]'
    )
    await next_button.click()

    # Verify that the form moved to Step 2
    progress = page.locator(
        '[data-testid="form-multi-step-progress"]'
    )
    await expect(progress).to_contain_text("Step 2 of 5")

    print("Step 3: Moved to Step 2.")

    # STEP 4: Return to the previous step
    back_button = page.locator(
        '[data-testid="form-multi-step-back"]'
    )
    await back_button.click()

    # STEP 5: Verify that the entered details were preserved
    await expect(first_name).to_have_value("Bhavya")
    await expect(email).to_have_value("bhavya.test@example.com")

    print("Step 4: Form data persistence verified.")
