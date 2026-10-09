import pytest

# @pytest.mark.asyncio
# async def test_typing(async_page):
#     try:
#         await async_page.goto("https://parabank.parasoft.com/parabank/index.htm")
#         register = async_page.get_by_text("Register")
#         await register.click()
#         fn = async_page.locator("//input[@id='customer.firstName']")
#         await fn.fill("Bhavya")
#         await async_page.wait_for_timeout(5000)
#         ln = async_page.locator("//input[@id='customer.lastName']")
#         await ln.type("Pathak")
#         add = async_page.locator("//input[@id='customer.address.street']")
#         await add.fill("CBT")
#         city = async_page.locator("//input[@id='customer.address.city']")
#         await city.type("Hubli")
#         state = async_page.locator("//input[@id='customer.address.state']")
#         await state.type("Karnataka")
#         zipcode =  async_page.locator("//input[@id='customer.address.zipCode']")
#         await zipcode.type("12345")
#         ph_num = async_page.locator("//input[@id='customer.phoneNumber']")
#         await ph_num.type("123678999")
#         ssn = async_page.locator("//input[@id='customer.ssn']")
#         await ssn.type("123456789")
#         un = async_page.locator("//input[@id='customer.username']")
#         await un.type("bhavya@123")
#         pwd = async_page.locator("//input[@id='customer.password']")
#         await pwd.fill("123456789")
#         cpwd = async_page.locator("//input[@id='repeatedPassword']")
#         await cpwd.fill("123456789")
#         submit = async_page.locator("(//input[@type='submit'])[2]")
#         await submit.click()
#         await async_page.wait_for_timeout(5000)
#         msg = async_page.locator("//p[text()='Your account was created successfully. You are now logged in.']")
#         await expect(msg).to_be_visible()
#         print(await msg.inner_text())
#         title = async_page.locator("//h1[@class='title']")
#         print(await title.inner_text())
#         await async_page.wait_for_timeout(5000)
#     except Exception as e:
#         print(e)



# @pytest.mark.asyncio
# async def test_ele_methods(async_page):
#     await async_page.goto("https://demowebshop.tricentis.com/")
#     ele =  async_page.get_by_text("Register")
#     text_of_ele = await ele.inner_text()
#     print("text of the ele is inner text" ,text_of_ele)
#     text_of_ele = await ele.inner_html()
#     print("text of the ele is html text", text_of_ele)
#     text_of_ele = await ele.text_content()
#     print("text of the ele is text content ", text_of_ele)
#     #get attribute
#     href = await ele.get_attribute("href")
#     print("get href attribute value is ", href)
#     class_ = await ele.get_attribute("class")
#     print("get class attribute value is ", class_)


# @pytest.mark.asyncio
# async def test_mul_ele_methods(async_page):
#     await async_page.goto("https://demowebshop.tricentis.com/")
#     products = async_page.locator("//h2[@class='product-title']")
#     print(products)
#     # await products.first.click()
#     # await async_page.wait_for_timeout(5000)
#     # await products.last.click()
#     # await async_page.wait_for_timeout(5000)
#     await products.nth(1).click()
#     await async_page.wait_for_timeout(5000)
   

# @pytest.mark.asyncio
# async def test_mul_ele_methods(async_page):
#     await async_page.goto("https://demowebshop.tricentis.com/books")
#     add_buttons_locator = async_page.locator("//input[@value='Add to cart']")
#     add_buttons = await add_buttons_locator.all()
#     for button in add_buttons:
#         await button.click()
#         await async_page.wait_for_timeout(2000)

# @pytest.mark.asyncio
# async def test_mul_ele_methods(async_page):
#     await async_page.goto("https://demowebshop.tricentis.com/books")
#     add_buttons_locator = async_page.locator("//input[@value='Add to cart']")
#     print(await add_buttons_locator.count())
#     add_buttons = await add_buttons_locator.all()
#     for button in add_buttons:
#         await button.click()
#         await async_page.wait_for_timeout(2000)


#books = ["Computing and Internet","Fiction","Health Book"]
@pytest.mark.asyncio
async def test_mul_ele_methods(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/books")
    # books = ["Computing and Internet", "Fiction", "Health Book"]
    books_name = "Fiction"
    book = async_page.locator(f"//a[text()='{books_name}']/../..//input[@value='Add to cart']")
    await book.click()
    await async_page.wait_for_timeout(2000)
    books = ["Computing and Internet", "Fiction", "Health Book"]
    for i in books:
        book = async_page.locator(f"//a[text()='{i}']/../..//input[@value='Add to cart']")
        await book.click()
        await async_page.wait_for_timeout(2000)

@pytest.mark.asyncio
async def test_mul_ele_methods(async_page):
    await async_page.goto("https://demowebshop.trice")