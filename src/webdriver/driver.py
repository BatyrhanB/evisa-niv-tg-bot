from selenium import webdriver

from decouple import config
from singleton import SingletonClass


class WebDriverSingleton(SingletonClass):
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

        self.driver.get(config("AEVISFORMS_URL"))
        self.driver.implicitly_wait(config("IMPLICITLY_WAIT"))

    def quit_driver(self) -> None:
        self.driver.quit()
