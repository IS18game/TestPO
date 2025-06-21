import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import os

def get_chrome_options():
    """Настройки Chrome для разных окружений"""
    options = Options()
    
    # Проверяем, запущены ли мы в GitHub Actions
    if os.getenv('GITHUB_ACTIONS'):
        # Headless режим для CI/CD
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
    else:
        # Обычный режим для локальной разработки
        options.add_argument('--start-maximized')
    
    return options

@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания драйвера Chrome"""
    options = get_chrome_options()
    
    # Используем webdriver-manager для автоматической установки драйвера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    
    # Закрываем браузер после каждого теста
    driver.quit()

@pytest.fixture(scope="function")
def bank_page(driver):
    """Фикстура для открытия страницы банка"""
    driver.get("http://localhost:8000/?balance=30000&reserved=20001")
    time.sleep(2)
    return driver

def wait_for_element(driver, by, value, timeout=10):
    """Вспомогательная функция для ожидания элементов"""
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable((by, value)))

def open_ruble_transfer(driver):
    """Открыть интерфейс перевода рублей"""
    # Нажимаем на рублевый счет
    ruble_account = wait_for_element(driver, By.XPATH, "//*[contains(text(), 'Рубли')]")
    ruble_account.click()
    time.sleep(1)

def enter_card_number(driver, card_number):
    """Ввести номер карты"""
    card_input = wait_for_element(driver, By.XPATH, "//input[@placeholder='Номер карты' or contains(@class, 'card') or @type='text']")
    card_input.clear()
    # Убираем пробелы из номера карты, так как приложение само форматирует
    card_number_clean = card_number.replace(" ", "")
    card_input.send_keys(card_number_clean)
    
    # Принудительно вызываем событие onChange через JavaScript
    driver.execute_script("""
        var event = new Event('input', { bubbles: true });
        arguments[0].dispatchEvent(event);
        var changeEvent = new Event('change', { bubbles: true });
        arguments[0].dispatchEvent(changeEvent);
    """, card_input)
    
    time.sleep(2)  # Увеличиваем время ожидания

def enter_transfer_amount(driver, amount):
    """Ввести сумму перевода"""
    # Поле суммы имеет placeholder='1000', а не 'Сумма'
    wait = WebDriverWait(driver, 10)
    amount_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='1000']")))
    
    amount_input.clear()
    amount_input.send_keys(str(amount))
    time.sleep(1)

def debug_dom_state(driver, step_name):
    """Отладочная функция для проверки состояния DOM"""
    print(f"\n=== DEBUG {step_name} ===")
    try:
        # Проверяем наличие поля карты
        card_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Номер карты' or contains(@class, 'card') or @type='text']")
        print(f"Поля карты найдено: {len(card_inputs)}")
        for i, inp in enumerate(card_inputs):
            print(f"  Поле {i+1}: value='{inp.get_attribute('value')}', placeholder='{inp.get_attribute('placeholder')}'")
        
        # Проверяем наличие полей суммы
        amount_inputs = driver.find_elements(By.XPATH, "//input")
        print(f"Всего input полей: {len(amount_inputs)}")
        for i, inp in enumerate(amount_inputs):
            placeholder = inp.get_attribute('placeholder')
            value = inp.get_attribute('value')
            if placeholder and ('сумма' in placeholder.lower() or '1000' in placeholder):
                print(f"  Поле суммы {i+1}: value='{value}', placeholder='{placeholder}'")
        
        # Проверяем текст на странице
        text_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Сумма') or contains(text(), 'сумма')]")
        print(f"Элементы с текстом 'Сумма': {len(text_elements)}")
        for elem in text_elements:
            print(f"  Текст: '{elem.text}'")
            
    except Exception as e:
        print(f"Ошибка при отладке: {e}")
    print("=== END DEBUG ===\n")

def debug_button_state(driver, step_name):
    """Отладочная функция для проверки состояния кнопки"""
    print(f"\n=== DEBUG BUTTON {step_name} ===")
    try:
        # Ищем все кнопки
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Всего кнопок найдено: {len(buttons)}")
        
        for i, btn in enumerate(buttons):
            text = btn.text
            class_name = btn.get_attribute("class")
            is_enabled = btn.is_enabled()
            is_displayed = btn.is_displayed()
            print(f"  Кнопка {i+1}: text='{text}', class='{class_name}', enabled={is_enabled}, displayed={is_displayed}")
            
            # Проверяем вложенные элементы
            spans = btn.find_elements(By.TAG_NAME, "span")
            for j, span in enumerate(spans):
                span_text = span.text
                print(f"    Span {j+1}: text='{span_text}'")
        
        # Ищем по тексту "перевести" (в любом регистре)
        transfer_buttons = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ПЕРЕВЕСТИ', 'перевести'), 'перевести')]")
        print(f"Элементы с текстом 'перевести': {len(transfer_buttons)}")
        for elem in transfer_buttons:
            print(f"  Элемент: tag='{elem.tag_name}', text='{elem.text}'")
            
    except Exception as e:
        print(f"Ошибка при отладке кнопки: {e}")
    print("=== END DEBUG BUTTON ===\n")

def find_transfer_button(driver):
    """Находит кнопку 'Перевести' по тексту внутри span или по классу"""
    # Пробуем найти по span с текстом
    try:
        return driver.find_element(By.XPATH, "//button[.//span[contains(translate(text(), 'ПЕРЕВЕСТИ', 'перевести'), 'перевести')]]")
    except:
        pass
    # Пробуем найти по классу
    try:
        return driver.find_element(By.XPATH, "//button[contains(@class, 'g-button') and contains(@class, 'outlined')]")
    except:
        pass
    # Пробуем найти любую кнопку с текстом 'Перевести'
    try:
        return driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ПЕРЕВЕСТИ', 'перевести'), 'перевести')]")
    except:
        pass
    raise Exception("Кнопка 'Перевести' не найдена")

def close_alert_if_present(driver):
    """Закрывает alert если он присутствует и возвращает его текст"""
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text
    except:
        return None

def click_transfer_button_safely(driver):
    """Безопасно кликает по кнопке 'Перевести' с обработкой alert"""
    try:
        transfer_button = find_transfer_button(driver)
        transfer_button.click()
        time.sleep(1)
        
        # Обрабатываем alert если он появился
        alert_text = close_alert_if_present(driver)
        return alert_text
    except Exception as e:
        # Если кнопка не найдена, возможно есть alert
        alert_text = close_alert_if_present(driver)
        if alert_text:
            return alert_text
        raise e