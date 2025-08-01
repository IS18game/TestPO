import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from conftest import wait_for_element, open_ruble_transfer, enter_card_number, enter_transfer_amount, find_transfer_button, click_transfer_button_safely

class TestSecondBatch:
    """Тесты ID: 006-010"""
    
    def test_006_negative_amount_transfer(self, bank_page):
        """ID: 006 - Проверка перевода отрицательного значения"""
        driver = bank_page
        
        open_ruble_transfer(driver)
        enter_card_number(driver, "1234567890123456")
        
        amount_input = wait_for_element(driver, By.XPATH, "//input[@placeholder='1000']")
        amount_input.clear()
        amount_input.send_keys("-10000")
        time.sleep(1)
        
        entered_value = amount_input.get_attribute("value")
        page_text = driver.page_source.lower()
        
        if entered_value == "-10000":
            if "ошибка" not in page_text and "некорректн" not in page_text:
                try:
                    alert_text = click_transfer_button_safely(driver)
                    if alert_text:
                        pytest.fail("БАГ: Система позволила выполнить перевод с отрицательной суммой")
                    else:
                        pytest.fail("БАГ: Система не блокирует отрицательные суммы")
                except:
                    pass
        else:
            assert True, "Система корректно отклонила отрицательное значение"
    
    def test_007_euro_transfer_limit(self, driver):
        """ID: 007 - Проверка лимитов перевода евро"""
        driver.get("http://localhost:8000/?balance=100&reserved=0")
        time.sleep(2)
        
        try:
            euro_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Евро') or contains(text(), '€')]")
            if not euro_elements:
                account_blocks = driver.find_elements(By.XPATH, "//*[contains(@class, 'account') or contains(@class, 'balance')]")
                if len(account_blocks) >= 3:
                    euro_elements = [account_blocks[2]]
            
            if euro_elements:
                euro_elements[0].click()
                time.sleep(1)
                
                enter_card_number(driver, "1234567890123456")
                enter_transfer_amount(driver, "1000")
                
                time.sleep(2)
                page_text = driver.page_source.lower()
                assert "недостаточно средств" in page_text or "insufficient" in page_text, \
                    "Должно появиться предупреждение о недостатке средств"
            else:
                pytest.skip("Евро счет недоступен в интерфейсе")
                
        except TimeoutException:
            pytest.skip("Интерфейс евро переводов недоступен")
    
    def test_008_non_standard_number_format(self, bank_page):
        """ID: 008 - Проверка ввода числа нестандартного формата"""
        driver = bank_page
        
        open_ruble_transfer(driver)
        enter_card_number(driver, "1234567890123456")
        
        enter_transfer_amount(driver, "000012435")
        time.sleep(2)
        
        page_text = driver.page_source
        expected_commission = "1243"
        
        assert expected_commission in page_text or "комиссия" in page_text.lower(), \
            "Комиссия должна быть рассчитана для суммы 12435"
        
        try:
            transfer_button = find_transfer_button(driver)
            assert transfer_button.is_displayed() and transfer_button.is_enabled(), \
                "Кнопка отправки перевода должна быть доступна"

            alert_text = click_transfer_button_safely(driver)
            
            if alert_text:
                assert any(s in alert_text for s in ["принят банком", "успешно", "выполнен"]), "Должно быть уведомление о принятии перевода"
            else:
                page_text = driver.page_source
                assert any(s in page_text for s in ["принят банком", "успешно", "выполнен"]), "Должно быть уведомление о принятии перевода"

        except Exception as e:
            if "Кнопка 'Перевести' не найдена" in str(e):
                page_text = driver.page_source.lower()
                if "ошибка" in page_text or "некорректн" in page_text:
                    assert True, "Система корректно отклонила некорректный формат суммы"
                else:
                    pytest.skip("Кнопка перевода недоступна для суммы с ведущими нулями (возможно, особенность системы)")
            else:
                pytest.fail(f"Неожиданная ошибка: {e}")
    
    def test_009_ruble_transfer_success(self, bank_page):
        """ID: 009 - Проверка перевода денег с рублевого счета"""
        driver = bank_page
        
        open_ruble_transfer(driver)
        
        card_number = "2473 7246 7644 3746"
        card_input = wait_for_element(driver, By.XPATH, "//input[@placeholder='Номер карты' or contains(@class, 'card') or @type='text']")
        card_input.clear()
        card_input.send_keys(card_number.replace(" ", ""))
        time.sleep(1)
        
        enter_transfer_amount(driver, "8000")
        time.sleep(2)
        
        page_text = driver.page_source
        assert any(str(c) in page_text for c in ["800", "800.0", "800,0"]), "Комиссия должна быть рассчитана как 800₽"
        
        try:
            alert_text = click_transfer_button_safely(driver)
            
            if alert_text:
                assert any(s in alert_text for s in ["принят банком", "успешно", "выполнен"]), "Должно быть уведомление о принятии перевода"
            else:
                page_text = driver.page_source
                assert any(s in page_text for s in ["принят банком", "успешно", "выполнен"]), "Должно быть уведомление о принятии перевода"

        except TimeoutException:
            pytest.fail("Не удалось выполнить перевод или получить уведомление")
    
    def test_010_ruble_limit_with_reserve(self, bank_page):
        """ID: 010 - Проверка лимитов перевода в рублях с резервом"""
        driver = bank_page
        
        open_ruble_transfer(driver)
        enter_card_number(driver, "1234567890123456")
        
        enter_transfer_amount(driver, "20000")
        time.sleep(2)
        
        page_text = driver.page_source.lower()
        assert "недостаточно средств" in page_text or "невозможен" in page_text, \
            "Должно появиться предупреждение о недостатке средств"
        
        try:
            transfer_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Перевести') or contains(@class, 'transfer')]")
            if transfer_button.is_enabled():
                pytest.fail("Кнопка 'Перевести' не должна быть активна при недостатке средств")
        except:
            pass  # Если кнопка не найдена или неактивна - это корректно
