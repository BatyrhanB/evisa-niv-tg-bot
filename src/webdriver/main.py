import time

from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from singleton import SingletonClass


class WebDriverSingleton(SingletonClass):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(config("AEVISFORMS_URL"))
        self.driver.implicitly_wait(5)

    def quit_driver(self):
        self.driver.quit()

class FormFiller(WebDriverSingleton):
    def fill_country(self, country_name):
        country_selector = self.driver.find_element(by=By.NAME, value="CountryCodeShow")
        country_select_object = Select(country_selector)
        country_select_object.select_by_visible_text(country_name)

    def fill_city(self, city_name):
        city_selector = self.driver.find_element(by=By.NAME, value="PostCodeShow")
        city_selected = Select(city_selector)
        city_selected.select_by_visible_text(city_name)

    def submit_form(self):
        submit = self.driver.find_element(by=By.NAME, value="Submit")
        submit.click()

    def fill_form(self, country_name, city_name):
        self.fill_country(country_name)
        self.fill_city(city_name)
        self.submit_form()

class MainApplication:
    def run(self):
        form_filler_instance = FormFiller()
        try:
            form_filler_instance.fill_form()
            time.sleep(8)
        finally:
            form_filler_instance.quit_driver()

if __name__ == "__main__":
    app = MainApplication()
    form_filler_instance = FormFiller()

    try:
        form_filler_instance.fill_country("KYRGYZSTAN")
        form_filler_instance.fill_city("BISHKEK")
        form_filler_instance.submit_form()
        time.sleep(8)
    finally:
        form_filler_instance.quit_driver()