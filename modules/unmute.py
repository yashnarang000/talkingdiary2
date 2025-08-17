from playwright.sync_api import sync_playwright
import time

class Unmute:

    def __init__(self, headless):
        '''
        headless: True or False
        '''
        self.headless = headless

    def play(self, prompt, voice, looping_condition):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=["--use-fake-ui-for-media-stream"],
            ignore_default_args=["--mute-audio"]
        )

        self.context = self.browser.new_context()
        self.context.grant_permissions(['microphone'])

        self.page = self.context.new_page()
        self.page.goto("https://unmute.sh/")

        self.prompt_area = self.page.locator("xpath=/html/body/div[1]/div/div/div[2]/div[2]/div/textarea")
        self.prompt_area.wait_for()
        self.prompt_area.fill(prompt)

        try:
            self.voice = self.page.locator(f"xpath=/html/body/div[1]/div/div/div[2]/div[2]/div/div[1]/div/button[{voice}]")
            while self.voice.wait_for(): print("Waiting...")
            self.voice.click()
        except:
            print("Voice not available!")

        self.play_button = self.page.locator("xpath=/html/body/div[1]/div/div/div[1]/div[1]/div/canvas")
        self.play_button.wait_for()
        self.play_button.click()
        while looping_condition: time.sleep(1)



if __name__ == "__main__":
    test_object = Unmute(headless=True)

    test_object.play(prompt="You are my senior developer in a coorporate world setting. Talk that way!",
                      voice=4,
                      looping_condition=True)