#work:---> 
#navigate to the facebook.com and validate title of the page
#navigate commands
#.env requirement files

# Sync mode
#from playwright.sync_api import sync_playwright, expect
#from playwright.async_api import async_playwright, expect
#import asyncio
import pytest





# def test_async_sync_exp1():
#   with sync_playwright() as p:
#     #chrome
#     browser = p.chromium.launch(headless=False)
#     user_context= browser.new_context()
#     page= user_context.new_page()
#     page.goto('https://facebook.com/')
#     print(page.title())
#     expect(page).to_have_title("Facebook")

#Async
#@pytest.mark.asyncio
#async def test_async_sync_exp2():
    #async with async_playwright() as p:
        #chrome
      #browser = await p.chromium.launch(headless=False)
      #user_context= await browser.new_context()
      #page= await user_context.new_page()
      #await page.goto('https://facebook.com/')
      #print(page.title())
      #await expect(page).to_have_title("Facebook")
      
#asyncio.run(test_async_sync_exp2())*/





# def test_async_sync_exp3(page):
#     page.goto('https://www.google.com/')
#     print(page.title())
#     expect(page).to_have_title("Google")
#     page.goto('https://www.google.in/')
#     page.go_back()
#     page.go_forward()
#     page.reload()

# @pytest.mark.asyncio
# async def test_async_sync_exp4(page):
#       await page.goto('https://facebook.com/')
#       print(page.title())
#       await expect(page).to_have_title("Facebook")

# def test_async_sync_exp3(page):
#     page.goto('https://www.google.com/')
#     print(page.title())

#     expect(page).to_have_title("Google")

#     page.goto('https://example.com/')
#     print("Google India:", page.url)

#     page.go_back()
#     print("After back:", page.url)

#     page.go_forward()
#     print("After forward:", page.url)


