from playwright.async_api import async_playwright
import time
import asyncio

async def main():
    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True,
            ignore_default_args = ["--mute-audio"],
            args = ["--use-fake-ui-for-media-stream"]
        )

        browserContext = await browser.new_context()
        await browserContext.grant_permissions(['microphone'])

        page = await browserContext.new_page()

        await page.goto("https://unmute.sh")

        voice = page.locator("xpath=/html/body/div[1]/div/div/div[2]/div[2]/div/div[1]/div/button[4]")
        await voice.click()

        play = page.locator("xpath=/html/body/div[1]/div/div/div[1]/div[1]/div/canvas")
        await play.click()

        print(await page.title())

        while True: time.sleep(1)

asyncio.run(main())