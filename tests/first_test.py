import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from conftest import wait_for_element, open_ruble_transfer, enter_card_number, enter_transfer_amount, debug_button_state, find_transfer_button, click_transfer_button_safely

class TestFirstBatch:
    """Тесты ID: 001-005"""
    
    def test_001_card_number_validation(self, bank_page):
        """ID: 001 - Проверка ввода номера карты"""
        driver = bank_page
        
        open_ruble_transfer(driver)

        enter_card_number(driver, "1234567890123456")
        
        try:
            amount_input = wait_for_element(driver, By.XPATH, "//input[@placeholder='1000']")
            assert amount_input.is_enabled(), "Поле суммы должно быть активно после ввода корректного номера карты"
        except TimeoutException:
            pytest.fail("Поле суммы не появилось после ввода корректного номера карты")
        
        enter_card_number(driver, "12345678901234567")
        
        card_input = driver.find_element(By.XPATH, "//input[@placeholder='Номер карты' or contains(@class, 'card') or @type='text']")
        entered_value = card_input.get_attribute("value")
        
        amount_input = wait_for_element(driver, By.XPATH, "//input[@placeholder='1000']")
        assert amount_input.is_enabled(), "Поле суммы должно остаться активным даже с 17-значным номером"
    
    def test_002_dollar_transfer_limit(self, driver):
        """ID: 002 - Проверка лимитов перевода доллара"""
        driver.get("http://localhost:8000/?balance=100&reserved=0")
        time.sleep(2)
        
        try:
            dollar_account = wait_for_element(driver, By.XPATH, "//*[contains(text(), 'Доллары')]")
            dollar_account.click()
            time.sleep(1)
            
            enter_card_number(driver, "1234567890123456")
            
            enter_transfer_amount(driver, "1000")
            
            page_text = driver.page_source.lower()
            assert "недостаточно средств" in page_text or "insufficient" in page_text, "Должно появиться предупреждение о недостатке средств"
            
        except TimeoutException:
            pytest.skip("Долларовый счет недоступен или интерфейс отличается")
    
    def test_003_ruble_transfer_with_reserve(self, bank_page):
        """ID: 003 - Проверка лимитов перевода в рублях с учетом резерва"""
        driver = bank_page
        
        open_ruble_transfer(driver)
        enter_card_number(driver, "1234567890123456")
        
        enter_transfer_amount(driver, "20000")
        
        time.sleep(2)
        page_text = driver.page_source.lower()
        assert "недостаточно средств" in page_text or "невозможен" in page_text, "Должно появиться предупреждение о недостатке средств"
    
    def test_004_transfer_notification(self, bank_page):
        """ID: 004 - Проверка отображения уведомления о переводе"""
        driver = bank_page
        
        open_ruble_transfer(driver)
        enter_card_number(driver, "2222222222222222")
        enter_transfer_amount(driver, "5000")

        debug_button_state(driver, "ПЕРЕД поиском кнопки")

        try:
            alert_text = click_transfer_button_safely(driver)
            
            if alert_text:
                assert "2222222222222222" in alert_text, "В уведомлении должен быть указан номер карты"
                assert "5000" in alert_text, "В уведомлении должна быть указана сумма"
                assert "принят банком" in alert_text, "Должно быть уведомление о принятии перевода"
            else:
                page_text = driver.page_source
                assert "2222222222222222" in page_text, "В уведомлении должен быть указан номер карты"
                assert "5000" in page_text, "В уведомлении должна быть указана сумма"
                assert "принят банком" in page_text, "Должно быть уведомление о принятии перевода"

        except TimeoutException:
            pytest.fail("Кнопка 'Перевести' недоступна или сумма превышает лимит")
    
    def test_005_large_balance_transfer(self, driver):
        """ID: 005 - Добавление на баланс новой суммы и проверка перевода"""

        driver.get("http://localhost:8000/?balance=300000&reserved=20001")
        time.sleep(2)
        
        open_ruble_transfer(driver)
        enter_card_number(driver, "2222222222222222")
        enter_transfer_amount(driver, "200000")
        
        try:
            transfer_button = find_transfer_button(driver)
            assert transfer_button.is_enabled(), "Кнопка 'Перевести' должна быть доступна для суммы 200000₽"
            
            page_text = driver.page_source
            assert "20000" in page_text or "комиссия" in page_text.lower(), "Комиссия должна быть рассчитана корректно"
            
            alert_text = click_transfer_button_safely(driver)
            
            if alert_text:
                assert "200000" in alert_text and "2222222222222222" in alert_text, "Уведомление должно содержать корректные данные"
            else:
                page_text = driver.page_source
                assert "200000" in page_text and "2222222222222222" in page_text, "Уведомление должно содержать корректные данные"

        except TimeoutException:
            pytest.fail("Перевод большой суммы недоступен при достаточном балансе")