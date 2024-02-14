import time

from decouple import config

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


driver = webdriver.Chrome()
driver.get(config("AEVISFORMS_URL"))
driver.implicitly_wait(5)

country_selector = driver.find_element(by=By.NAME, value="CountryCodeShow")
country_select_object = Select(country_selector)
country_select_object.select_by_visible_text("KYRGYZSTAN")

city_selector = (driver.find_element(by=By.NAME, value="PostCodeShow"))
city_selected = Select(city_selector)
city_selected.select_by_visible_text("BISHKEK")

submit = driver.find_element(by=By.NAME, value="Submit")
submit.click()


time.sleep(8)

driver.quit()