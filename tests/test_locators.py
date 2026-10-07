# import playwright.async_api as playwright
# import pytest
# from dotenv import load_dotenv
# import os
# load_dotenv()


# @pytest.mark.asyncio
# async def test_evn_(async_page):
#     await async_page.goto(os.getenv("BASE_URL"))
#     print(await async_page.title())

# import playwright.async_api as playwright
from playwright.async_api import expect
import pytest
# from utils.config import BASE_URL,USERNAME,PASSWORD
# from dotenv import load_dotenv
# import os

#load_dotenv()


# @pytest.mark.asyncio
# async def test_env(async_page):
#     print("BASE_URL:", os.getenv("BASE_URL"))
#     await async_page.goto(os.getenv("BASE_URL"))
#     print(await async_page.title())


# @pytest.mark.asyncio
# async def test_getbyrole(async_page):
#     await async_page.goto("https://demowebshop.tricentis.com/")
#     reg_link = async_page.get_by_role("link",name = "Register")
#     await expect(reg_link).to_be_visible()
#     await reg_link.click()
#     await expect(async_page).to_have_title("Demo Web Shop. Register")


# @pytest.mark.asyncio
# async def test_getByText(async_page):
#    await async_page.goto("https://demowebshop.tricentis.com/")
#    excellent = async_page.get_by_text("Excellent")
#    await expect(excellent).not_to_be_checked()
#    await excellent.click()
#    await expect(excellent).to_be_checked()
#    await async_page.wait_for_timeout(5000)
#    vb =  async_page.get_by_role("radio",name="Very bad")
#    await expect(vb).to_be_visible()
#    await vb.click()

# # page.getByLabel() to locate a form control by associated label's text.
# @pytest.mark.asyncio
# async def test_getBylabel(async_page):
#    await async_page.goto("https://demowebshop.tricentis.com/")
#    reg_link =  async_page.get_by_text("Register")
#    await expect(reg_link).to_be_visible()
#    await reg_link.click()
#    g = async_page.get_by_text("Female")
#    await expect(g).to_be_visible()
#    await g.click()
#    fn = async_page.get_by_label("First name:")
#    await expect(fn).to_be_visible()
#    await fn.fill("Abc")
#    ln = async_page.get_by_label("Last name:")
#    await expect(ln).to_be_visible()
#    await ln.fill("Abc")
#    email = async_page.get_by_label("Email:")
#    await expect(email).to_be_visible()
#    await email.fill("abc@gmail.com")
#    pwd = async_page.get_by_label("Password:").nth(0) # [pwd,cpwd]
#    await expect(pwd).to_be_visible()
#    await pwd.fill("Abc@123")
#    cpwd = async_page.get_by_label("Confirm password:")
#    await expect(cpwd).to_be_visible()
#    await cpwd.fill("Abc@123")


# page.getByPlaceholder() to locate an input by placeholder.
# @pytest.mark.asyncio
# async def test_getByPlaceholder(async_page):
#    await async_page.goto("https://demowebshop.tricentis.com/")
#    search_tb = async_page.get_by_placeholder("Search store")
#    await expect(search_tb).to_be_visible()
#    await search_tb.fill("Books")
#    print(search_tb.input_value())

# @pytest.mark.asyncio
# async def test_getByalt_text(async_page):
#    await async_page.goto("https://demowebshop.tricentis.com/")
#    img = async_page.get_by_alt_text("Picture of 14.1-inch Laptop")
#    await expect(img).to_be_visible()
#    await img.click()
#    await expect(async_page).to_have_url("https://demowebshop.tricentis.com/141-inch-laptop")


# @pytest.mark.asyncio
# async def test_getBytitle(async_page):
#    await async_page.goto("https://demowebshop.tricentis.com/")
#    ele = async_page.locator("h2[class='topic-html-content-header']") # locator :notfinding
#    await expect(ele).to_be_visible()
#    print(await ele.inner_html())

# @pytest.mark.asyncio
# async def test_getBytitle(async_page):
#    await async_page.goto("https://demowebshop.tricentis.com/books")
#    ele = async_page.locator(".product-title") # locator :notfinding
#    # ele :-- all products
#    all_product = await ele.all()
#    for i in all_product:
#        print(await i.inner_text())
   

# @pytest.mark.asyncio
# async def test_getBytitle(async_page):
#    await async_page.goto("https://demowebshop.tricentis.com/")
#    ele = async_page.locator("input[class='button-2 product-box-add-to-cart-button']") # locator :notfinding
#    all_product = await ele.all()
#    for i in all_product:
#       await i.click()
#       break
#    await async_page.wait_for_timeout(5000)

   #xpath types

   #xpath by attribute
   # //tagName[@attribute='Value']

   #xpath by text
   # //tagName[text()='Text']

   #Xpath by contains
   # //tagName[contains(attribute,value)]
   #//tagName[contains(text(),text)]

   # Xpath by Group
   # (xpath)[index_num]


   #  * -> contains
   # ^ -> start with
   #  $ -> end with