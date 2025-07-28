from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        ignore_default_args=["--mute-audio"]
    )
    
    page = browser.new_page()
    page.goto("https://santar.webflow.io/")
    button = page.locator("xpath=/html/body/div[3]/div[3]/div[3]/a[2]/img")
    button.click()
    print(page.title())
    time.sleep(30)
    browser.close