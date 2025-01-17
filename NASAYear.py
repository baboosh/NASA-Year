import rumps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time

class NASAYearApp(rumps.App):
    def __init__(self):
        super(NASAYearApp, self).__init__("NASA YEAR: ----", quit_button=None) 
        self.driver = None
        self.setup_browser()
        self.menu = ["stop scientifically tracking the year", "link to source data"] 
        
    def setup_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://iss-mimic.github.io/Mimic/")
        
    def update_year(self):
        while True:
            try:
                year_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "TIME_000002"))
                )
                year = year_element.text
                self.title = f"NASA YEAR: {year}"
                time.sleep(5)
            except Exception as e:
                print(f"Error: {e}")
                self.title = "NASA YEAR: ERROR"
                self.driver.quit()
                self.setup_browser()
                time.sleep(5)
    
    @rumps.clicked("stop scientifically tracking the year")
    def quit(self, _):
        self.driver.quit()
        rumps.quit_application()

    @rumps.clicked("link to source data")
    def linkSource(self, _):
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://iss-mimic.github.io/Mimic/")

if __name__ == "__main__":
    app = NASAYearApp()
    threading.Thread(target=app.update_year, daemon=True).start()
    app.run()
