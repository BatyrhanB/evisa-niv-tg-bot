from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver import WebDriverSingleton


class FormFiller:
    def __init__(self, driver):
        self.driver = driver

    def fill_field(self, field_name: str, value: str) -> None:
        field_selector = self.driver.find_element(by=By.NAME, value=field_name)
        field_select_object = Select(field_selector)
        field_select_object.select_by_visible_text(value)

    def submit_form(self) -> None:
        submit_button = self.driver.find_element(by=By.NAME, value="Submit")
        submit_button.click()


class CaptchaBreaker:
    def __init__(self, driver):
        self.driver = driver

    def get_captcha_image_source(self, xpath):
        try:
            captcha_image_source = self.driver.find_element(
                by=By.XPATH, value=xpath
            ).get_attribute("src")
        except:
            captcha_image_source = None
        return captcha_image_source

    def solve_captcha(self, captcha_source, input_locator):
        #solved_word = captcha_breaker(captcha_source)

        input_field = self.driver.find_element(
            by=input_locator["by"], value=input_locator["value"]
        )
        #print("HEREEEEEEEEEEEEEEE", solved_word)
        #input_field.send_keys(solved_word)

    def determine_captcha_type(self, xpath1, xpath2, input_locator1, input_locator2):
        captcha_source1 = self.get_captcha_image_source(xpath1)
        captcha_source2 = self.get_captcha_image_source(xpath2)

        if captcha_source1:
            self.solve_captcha(captcha_source1, input_locator1)
            submit_captcha = self.driver.find_element(
                by=By.XPATH,
                value="/html/body/form/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[3]/input[2]",
            )
            submit_captcha.click()
            print("Solved captcha on the first type of page.")
        elif captcha_source2:
            self.solve_captcha(captcha_source2, input_locator2)
            submit_captcha = self.driver.find_element(
                by=By.XPATH, value="/html/body/button"
            )
            submit_captcha.click()
            print("Solved captcha on the second type of page.")
        else:
            print("Not redirected to any captcha page.")


class MainApplication:
    def run(self):
        with WebDriverSingleton() as driver_instance:
            form_filler = FormFiller(driver_instance.driver)
            captcha_breaker = CaptchaBreaker(driver_instance.driver)

            try:
                form_filler.fill_field("CountryCodeShow", "KYRGYZSTAN")
                form_filler.fill_field("PostCodeShow", "BISHKEK")
                form_filler.submit_form()

                WebDriverWait(driver_instance.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='frmconinput_CaptchaImage']")
                    )
                    or EC.presence_of_element_located((By.XPATH, "/html/body/img"))
                )

                captcha_breaker.determine_captcha_type(
                    "//*[@id='frmconinput_CaptchaImage']",
                    "/html/body/img",
                    {
                        "by": By.XPATH,
                        "value": "/html/body/form/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[3]/input[1]",
                    },
                    {"by": By.XPATH, "value": "/html/body/input"},
                )
            finally:
                driver_instance.quit_driver()


if __name__ == "__main__":
    app = MainApplication()
    app.run()
