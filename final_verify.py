import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        file_path = "file://" + os.path.abspath("111.html")
        await page.goto(file_path)

        # Check all "Mercury Smart Energy" occurrences
        content = await page.content()
        count = content.count("Mercury Smart Energy")
        print(f"Found {count} occurrences of 'Mercury Smart Energy'")

        # Check header
        header_text = await page.locator("header").inner_text()
        if "Mercury Smart Energy" in header_text:
            print("✓ Header branding updated.")

        # Check hero
        hero_text = await page.locator("h1").first.inner_text()
        if "Mercury Smart Energy" in hero_text:
            print("✓ Hero branding updated.")

        # Check navigation
        await page.locator("button:has-text('Подробнее')").first.click()
        await page.wait_for_selector("text=Назад на главную")
        print("✓ News detail from Home shows 'Назад на главную'")
        await page.click("text=Назад на главную")

        await page.click("[data-nav='news']")
        await page.locator("button:has-text('Читать статью')").first.click()
        await page.wait_for_selector("text=Назад к новостям")
        print("✓ News detail from News shows 'Назад к новостям'")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
