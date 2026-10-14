import pytest
from playwright.async_api import expect
# from pathlib import Path


# @pytest.mark.asyncio
# async def test_freams(async_page):
#     await async_page.goto("https://jqueryui.com/datepicker/")

#     frame = async_page.frame_locator(".demo-frame")

#     await frame.locator("//input[@id='datepicker']").click()
#     await frame.locator("//a[text()='14']").click()


# @pytest.mark.asyncio
# async def test_file_upload(async_page):
#     await async_page.goto("https://practice.expandtesting.com/upload#google_vignette")
#     await async_page.locator("#fileInput").set_input_files("C:/Users/User/Downloads/test.docx")
#     await async_page.wait_for_timeout(5000)
#     await async_page.locator("#fileSubmit").click()
#     # msg = async_page.get_by_text("File Uploaded!")
#     # await expect(msg).to_be_visible()


# @pytest.mark.asyncio
# async def test_file_download(async_page):
#     await async_page.goto("https://demo.automationtesting.in/FileDownload.html#google_vignette")
#     # down file:-->
#     download_dir = (Path("downloads"))
#     download_dir.mkdir(parents=True, exist_ok=True)

#     async with async_page.expect_download() as download_dir_info:
#         await async_page.locator("(//a[text()='Download'])[1]").click()

#     download_ = await download_dir_info.value
#     save_path = download_dir / download_.suggested_filename
#     await download_.save_as(str(save_path))
#     print("file downloaded = " , save_path)
#     print("file is exists " , save_path.exists())
#     print("down failed" , await download_.failure())

@pytest.mark.asyncio
async def test_mouse_hover(async_page):
    await async_page.goto("https://demowebshop.tricentis.com/")
    await async_page.locator("(//a[contains(text(),'Computers')])[1]").hover()
    await async_page.locator("(//a[contains(text(),'Desktops')])[1]").click()
    ele = async_page.locator("//h1[text()='Desktops']")
    await expect(ele).to_be_visible()


@pytest.mark.asyncio
async def test_du_clk(async_page):
    await async_page.goto("https://testautomationpractice.blogspot.com/")
    await async_page.locator("//button[text()='Copy Text']").dblclick()
    print(await async_page.locator("#field2").input_value())

@pytest.mark.asyncio
async def test_right_clk(async_page):
    await async_page.goto("https://testautomationpractice.blogspot.com/")
    await async_page.locator("//button[text()='Copy Text']").click(button="right")
    await async_page.wait_for_timeout(5000)