import os
import time
import threading
import tkinter as tk
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = "rw.powerapps@bboxx.com"
password = "Ny7NYHVgMbg9#KYXW"

class Browser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--kiosk")
        # webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options)
        self.options = chrome_options
        self.initialize_browser()

    def initialize_browser(self):
        self.browser = webdriver.Chrome(options=self.options)


    def open_page(self, url: str):
        self.browser.get(url)

    def close_browser(self):
        self.browser.quit()  # Use quit() instead of close() for proper cleanup

    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)

    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(1)

    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        wait = WebDriverWait(self.browser, timeout)
        return wait.until(EC.visibility_of_element_located((by, value)))

    def login_username(self, username: str):
        self.add_input(by=By.ID, value="i0116", text=username)
        self.click_button(by=By.ID, value="idSIButton9")

    def login_password(self, password: str):
        self.add_input(by=By.ID, value="i0118", text=password)
        self.click_button(by=By.ID, value="idSIButton9")
        time.sleep(1)

    def login_click1(self):
        self.click_button(by=By.ID, value="idSIButton9")


class ScriptRunner:
    def __init__(self):
        self.browser = Browser()
        self.is_running = False
        self.thread = None

    def start_script(self):
        if self.is_running:
            return

        self.is_running = True
        self.thread = threading.Thread(target=self.run_script)
        self.thread.start()

    def stop_script(self):
        if not self.is_running:
            return

        self.is_running = False
        self.thread.join()
        self.browser.close_browser()

    def run_script(self):
        self.browser.open_page("https://apps.powerapps.com/play/e/bbc6cd3f-3248-e7e9-acea-1e78f4722344/a/65ea030b-7a6d-4ba7-bfd2-c310aa606e90?tenantId=85564f10-ae91-478e-82b2-71d5eb2aecf2&sourcetime=1694592550225&hidenavbar=true")
        self.browser.wait_for_element(By.ID, "i0116")
        self.browser.login_username(username)
        
        if not self.is_running:
            return

        self.browser.wait_for_element(By.ID, "i0118")
        self.browser.login_password(password)
        
        if not self.is_running:
            return

        self.browser.wait_for_element(By.ID, "idSIButton9")
        self.browser.login_click1()

        while self.is_running:
            time.sleep(1)
        self.browser.close_browser()


if __name__ == '__main__':
    script_runner = ScriptRunner()

    def start_script():
        if script_runner.is_running:
            stop_script()
        script_runner.start_script()

    def stop_script():
        script_runner.stop_script()

    root = tk.Tk()
    root.title("Script Runner")
    root.attributes("-topmost", True)  # Set the window to always be on top

    start_button = tk.Button(root, text="Start Script", command=start_script)  # Renamed button text
    start_button.pack()

    stop_button = tk.Button(root, text="Stop Script", command=stop_script)  # Renamed button text
    stop_button.pack()

    root.mainloop()
