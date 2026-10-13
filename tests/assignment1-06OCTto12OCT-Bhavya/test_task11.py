
import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_extracting_text_and_attributes():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://demowebshop.tricentis.com/")

        # 1. Locate a heading and retrieve its text
        heading = page.locator("h2 a").first
        heading_text = await heading.text_content()

        print("Heading text:", heading_text)

        # Verify the heading text
        assert heading_text is not None
        assert heading_text.strip() != ""

        # 2. Retrieve inner text from a container
        container = page.locator(".header")
        container_text = await container.inner_text()

        print("Header container text:", container_text)

        # Verify that the container has text
        assert container_text.strip() != ""

        # 3. Retrieve an input field's value
        search_box = page.locator("#small-searchterms")
        await search_box.fill("computer")

        input_value = await search_box.input_value()

        print("Input value:", input_value)

        # Verify the input value
        assert input_value == "computer"

        # 4. Read two HTML attributes
        input_class = await search_box.get_attribute("class")
        input_type = await search_box.get_attribute("type")

        print("Input class:", input_class)
        print("Input type:", input_type)

        # Verify the attributes
        assert input_class is not None
        assert input_type == "text"

        # 5. Retrieve a link's href attribute
        link = page.locator(".header-logo a")
        href_value = await link.get_attribute("href")

        print("Logo link href:", href_value)

        # Verify the href
        assert href_value == "/"

        await browser.close()
