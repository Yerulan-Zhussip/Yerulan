import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Using a local file path
        import os
        path = "file://" + os.path.abspath("111.html")
        await page.goto(path)

        # 1. Check Hero Banner height
        hero = await page.query_selector('.hero-bg')
        hero_box = await hero.bounding_box()
        print(f"Hero height: {hero_box['height']}px")

        # 2. Check News Card height
        news_card = await page.query_selector('.news-slide')
        news_box = await news_card.bounding_box()
        print(f"News card height: {news_box['height']}px")

        # 3. Check for "( О компании кратко )"
        content = await page.content()
        if "О компании кратко" in content:
            print("FAIL: '( О компании кратко )' still exists")
        else:
            print("SUCCESS: '( О компании кратко )' removed")

        # 4. Check for Prices button in header
        header_btns = await page.query_selector_all('header button, header a')
        prices_btn_found = False
        for btn in header_btns:
            text = await btn.inner_text()
            if "Цены" in text:
                prices_btn_found = True
                break
        if prices_btn_found:
            print("FAIL: 'Prices' button still in header")
        else:
            print("SUCCESS: 'Prices' button removed from header")

        # 5. Check Price Section content
        if "Дизельное топливо" in content and "Авиатопливо и бензин" in content:
            print("SUCCESS: Price section categories found")

        await page.screenshot(path="final_verification.png")
        await browser.close()

asyncio.run(verify())
