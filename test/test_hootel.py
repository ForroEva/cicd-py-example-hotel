import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import allure
import pytest
import random


class TestHootel(object):
    def setup_method(self):
        URL = 'http://hotel-v3.progmasters.hu/'
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    @pytest.mark.parametrize("email, password", [('progmtest4@proton.me', 'ProgMtest4')])
    @allure.title("Hootel Login")
    @allure.description("A belépés tesztelése")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.tag("login")
    def test_login(self, email, password):
        menu_toggle = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, "//button[@class = 'navbar-toggler collapsed']")))
        menu_toggle.click()
        login_btn = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))
        login_btn.click()

        time.sleep(0.5)
        email_input = self.browser.find_element(By.ID, 'email')
        email_input.send_keys(email)

        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys(password)

        submit_btn = self.browser.find_element(By.NAME, 'submit')
        submit_btn.click()

        logout_btn = WebDriverWait(self.browser, 5).until(ec.element_to_be_clickable((By.ID, "logout-link")))

        assert logout_btn.text == "Kilépés"

    def test_hotel_list(self):
        hotel_list_btn = self.browser.find_element(By.XPATH, '//button[@class="btn btn-outline-primary btn-block"]')
        hotel_list_btn.click()
        time.sleep(1)

        hotel_list = self.browser.find_elements(By.XPATH, '//h4[@style="cursor: pointer"]')
        assert len(hotel_list) != 0
        assert len(hotel_list) == 10

    def test_hotel_checkbox(self):
        checkbox_list = self.browser.find_elements(By.XPATH, '//input[@type="checkbox"]')
        for checkbox in checkbox_list:
            checkbox.click()
            assert checkbox.is_selected()

        erase_selection_btn = self.browser.find_element(By.ID, 'redstar')
        erase_selection_btn.click()

        for checkbox in checkbox_list:
            check_class = checkbox.get_attribute('class')
            if 'ng-pristine' in check_class:
                print('A checkbox nincs kijelölve.')

    def test_chose_hotel (self):
        first_hotel = self.browser.find_element(By.XPATH, '//h4[@style="cursor: pointer"]')
            first_hotel.click()
            time.sleep(1)

    def test_hotel_descriptin(self):
        hotel_description = self.browser.find_elements(By.XPATH, '//p[@class="card-text"]')[1]
        print(hotel_description.text)
        assert 500 <= len(hotel_description.text) <= 2000

    def test_booking(self):
        booking_btn = self.browser.find_element(By.ID, 'user-bookings')
        booking_btn.click()
        time.sleep(2)

        erase_actual_booking_btn = self.browser.find_elements(By.XPATH, '//div[@id="actual"]//button')
        erase_past_booking_btn = self.browser.find_elements(By.XPATH, '//div[@id="past"]//button')

        if len(erase_actual_booking_btn) >= 1:
            print(f'A felhasználónak van jelenlegi foglalása: {len(erase_actual_booking_btn)} db.')
        else:
            print('A felhasználónak nincs jelenlegi foglalása.')

        if len(erase_past_booking_btn) >= 1:
            print(f'A felhasználónak van múltbeli foglalása: {len(erase_past_booking_btn)} db.')
        else:
            print('A felhasználónak nincs múltbeli foglalása.')

        browser.quit()
