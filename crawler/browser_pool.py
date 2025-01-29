from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fp.fp import FreeProxy
import random

class BrowserPool:
    def __init__(self, pool_size=5, headless=True):
        self.pool = []
        self.proxy = FreeProxy()
        self.user_agents = self.load_user_agents()
        self.init_pool(pool_size, headless)

    def init_pool(self, size, headless):
        for _ in range(size):
            options = Options()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument(f"user-agent={random.choice(self.user_agents)}")
            options.add_argument(f"--proxy-server={self.proxy.get()}")
            driver = webdriver.Chrome(options=options)
            self.pool.append(driver)

    def get_browser(self):
        while True:
            for driver in self.pool:
                if not driver.current_url:
                    return driver
            self.rotate_proxies()

    def rotate_proxies(self):
        for driver in self.pool:
            driver.quit()
        self.init_pool(len(self.pool), True)

    def load_user_agents(self):
        return [
           
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
           
        ]

class BrowserManager:
    def __init__(self):
        self.pool = BrowserPool()
        
    def render_page(self, url):
        driver = self.pool.get_browser()
        try:
            driver.get(url)
            return driver.page_source
        finally:
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
