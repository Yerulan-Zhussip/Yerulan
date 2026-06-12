import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        path = "file://" + os.path.abspath("111.html")
        await page.goto(path)
        await page.screenshot(path="screenshot_ui.png")
        await browser.close()

asyncio.run(verify())
