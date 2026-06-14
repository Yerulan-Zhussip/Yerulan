import os
import asyncio
from playwright.async_api import async_playwright

async def run_verification():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Get absolute path to 111.html
        file_path = "file://" + os.path.abspath("111.html")
        await page.goto(file_path)

        print("Page loaded.")

        # 1. Login as Admin
        # Use a more generic selector if the previous one failed
        await page.wait_for_selector('button:has-text("Вход")', timeout=5000)
        await page.click('button:has-text("Вход")')
        await page.wait_for_selector('#username', timeout=5000)
        await page.fill('#username', 'admin')
        await page.fill('#password', 'admin')
        await page.click('button[type="submit"]')
        print("Logged in as Admin.")

        # 2. Check for "My Cabinet" and "Edit Prices" buttons
        await page.wait_for_selector('[data-nav="profile"]')
        print("Found My Cabinet button.")

        await page.wait_for_selector('#editPricesBtn')
        print("Found Edit Prices button.")

        # 3. Open My Cabinet
        await page.click('[data-nav="profile"]')
        await page.wait_for_selector('h2:has-text("Админ Главный")')
        print("Verified Profile Page content.")

        # 4. Create a restricted user
        await page.click('#addUserBtn')
        await page.fill('#newUsername', 'testuser')
        await page.fill('#newPassword', 'password')
        await page.fill('#newLastName', 'User')
        await page.fill('#newFirstName', 'Test')
        await page.fill('#newPosition', 'Worker')
        await page.fill('#newCabinet', '202')
        await page.fill('#newBirthDate', '1995-05-05')

        # Set permissions: can only view Reservoir #1, no edit prices, no add news
        await page.click('#tankAccessSome')
        # Wait for checkboxes to be enabled
        await page.wait_for_timeout(500)
        await page.check('input[name="tankId"][value="1"]')

        # Submit
        page.on("dialog", lambda dialog: dialog.accept())
        await page.click('button:has-text("Создать аккаунт")')
        print("Created restricted user.")

        # 5. Logout and Login as testuser
        await page.click('#logoutBtn')
        await page.click('[data-nav="login"]')
        await page.fill('#username', 'testuser')
        await page.fill('#password', 'password')
        await page.click('button[type="submit"]')
        print("Logged in as testuser.")

        # 6. Verify restrictions
        # Should NOT see Edit Prices button
        edit_prices_btn = await page.query_selector('#editPricesBtn')
        assert edit_prices_btn is None, "Edit Prices button should NOT be visible"
        print("Verified: Edit Prices button hidden for testuser.")

        # Should NOT see Add News button (homeAddNewsBtn)
        add_news_btn = await page.query_selector('#homeAddNewsBtn')
        assert add_news_btn is None, "Add News button should NOT be visible"
        print("Verified: Add News button hidden for testuser.")

        # Should only see Reservoir #1 on Tanks page
        await page.click('[data-nav="tanks"]')
        await page.wait_for_selector('.tank')
        tanks = await page.query_selector_all('.tank')
        assert len(tanks) == 1, f"Should only see 1 tank, found {len(tanks)}"
        tank_name = await tanks[0].inner_text()
        assert "Резервуар №1" in tank_name, f"Expected Reservoir #1, found {tank_name}"
        print("Verified: Tank visibility restricted.")

        # Should NOT see Save Changes button
        save_btn = await page.query_selector('#saveTanksBtn')
        assert save_btn is None, "Save Changes button should NOT be visible"
        print("Verified: Tank editing restricted.")

        await browser.close()
        print("Verification complete successfully.")

if __name__ == "__main__":
    asyncio.run(run_verification())
