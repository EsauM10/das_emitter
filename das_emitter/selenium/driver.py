import os

import undetected_chromedriver as webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ChromeDecorator(webdriver.Chrome):
    def __del__(self):
        try:
            return super().__del__()
        except: pass        

class SeleniumDriver:
    def __init__(self, headless: bool = True) -> None:
        self.download_path = os.path.join(os.getcwd(), 'data')
        self.__driver = ChromeDecorator(options=self.__make_options(headless))

    def __make_options(self, headless: bool) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        options.add_experimental_option('prefs', {
            'download.default_directory': self.download_path,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'plugins.always_open_pdf_externally': True
        })

        if(headless):
            options.add_argument('--headless')
        return options
    
    def goto(self, url: str):
        self.__driver.get(url)

    def await_element(self, selector: str, timeout: float = 1) -> WebElement:
        return WebDriverWait(self.__driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, selector))
        )
    
    def find_element(self, selector: str) -> WebElement:
        return self.__driver.find_element(By.XPATH, value=selector)

    def close(self):
        self.__driver.close()