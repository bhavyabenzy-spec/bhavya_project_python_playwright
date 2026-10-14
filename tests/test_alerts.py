# import asyncio
# import pytest
# from playwright.async_api import expect

# @pytest.mark.asyncio
# async def test_check_box_input_list(async_page):
#     await async_page.goto("https://testautomationpractice.blogspot.com/")

#     async_page.once(
#         "dialog",
#         lambda dialog: asyncio.create_task(dialog.accept())
#     )

#     await async_page.get_by_text("Simple Alert").click()

#     ele = async_page.locator("#sunday")
#     await expect(ele).not_to_be_checked()
#     await ele.click()
#     await expect(ele).to_be_checked()


#     async def handle_aletrs(dialog):
#     print("alert type = " , dialog.type)
#     print("alter msg" , dialog.message)
#     await dialog.accept()


import pytest
from playwright.async_api import expect

# async def handle_aletrs(dialog):
#     print("alert type = " , dialog.type)
#     print("alter msg" , dialog.message)
#     await dialog.accept()


# @pytest.mark.asyncio
# async def test_check_box_input_list(async_page):
#     await async_page.goto("https://testautomationpractice.blogspot.com/")
#     async_page.on("dialog", handle_aletrs)
#     await async_page.get_by_text("Simple Alert").click()

#     ele = async_page.locator("#sunday")
#     await  expect(ele).not_to_be_checked()
#     await ele.click()
#     await  expect(ele).to_be_checked()


# async def handle_aletrs(dialog):
#     print("alert type = " , dialog.type)
#     print("alter msg" , dialog.message)
#     await dialog.accept()


# @pytest.mark.asyncio
# async def test_alert(async_page):
#     await async_page.goto("https://testautomationpractice.blogspot.com/")
#     async_page.on("dialog", handle_aletrs)
#     await async_page.get_by_text("Confirmation Alert").click()

#     ele = async_page.locator("#sunday")
#     await  expect(ele).not_to_be_checked()
#     await ele.click()
#     await  expect(ele).to_be_checked()



# async def handle_aletrs(dialog):
#     print("alert type = " , dialog.type)
#     print("alter msg" , dialog.message)
#     await dialog.accept("Demo")


# @pytest.mark.asyncio
# async def test_alert(async_page):
#     await async_page.goto("https://testautomationpractice.blogspot.com/")
#     async_page.on("dialog", handle_aletrs)
#     await async_page.get_by_text("Prompt Alert").click()

#     ele = async_page.get_by_text("Hello Demo! How are you today?")
#     await  expect(ele).to_be_visible()


@pytest.mark.asyncio
async def test_mul_wiind(async_page):
    await async_page.goto("https://www.amazon.in/")
    search_box = async_page.locator("#twotabsearchtextbox")
    await search_box.fill("Books")
    await search_box.press("Enter")
    await async_page.wait_for_timeout(5000)
    books = async_page.locator("//h2[@class='a-size-medium a-spacing-none a-color-base a-text-normal']")

    # need get the wind info
    async with async_page.expect_popup() as pop_info:
        await books.first.click()
        
    product_page = await pop_info.value
    await product_page.locator("//input[@id='add-to-cart-button']").click()