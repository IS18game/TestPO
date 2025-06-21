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
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', '')),
    ]
    
    chrome_binary = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_binary = path
            break
    
    if chrome_binary:
        options.binary_location = chrome_binary
    
    if os.getenv('GITHUB_ACTIONS'):
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
    else:
        options.add_argument('--start-maximized')
    
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    options.add_argument('--disable-javascript')
    options.add_argument('--no-first-run')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    
    return options

@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания драйвера Chrome"""
    options = get_chrome_options()
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Ошибка при создании драйвера с ChromeDriverManager: {e}")
        try:
            driver = webdriver.Chrome(options=options)
        except Exception as e2:
            print(f"Ошибка при создании драйвера без service: {e2}")
            basic_options = Options()
            basic_options.add_argument('--headless')
            basic_options.add_argument('--no-sandbox')
            basic_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=basic_options)
    
    yield driver
    
    try:
        driver.quit()
    except:
        pass

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
    ruble_account = wait_for_element(driver, By.XPATH, "//*[contains(text(), 'Рубли')]")
    ruble_account.click()
    time.sleep(1)

def enter_card_number(driver, card_number):
    """Ввести номер карты"""
    card_input = wait_for_element(driver, By.XPATH, "//input[@placeholder='Номер карты' or contains(@class, 'card') or @type='text']")
    card_input.clear()
    card_number_clean = card_number.replace(" ", "")
    card_input.send_keys(card_number_clean)
    
    driver.execute_script("""
        var event = new Event('input', { bubbles: true });
        arguments[0].dispatchEvent(event);
        var changeEvent = new Event('change', { bubbles: true });
        arguments[0].dispatchEvent(changeEvent);
    """, card_input)
    
    time.sleep(2)

def enter_transfer_amount(driver, amount):
    """Ввести сумму перевода"""
    wait = WebDriverWait(driver, 10)
    amount_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='1000']")))
    
    amount_input.clear()
    amount_input.send_keys(str(amount))
    time.sleep(1)

def debug_dom_state(driver, step_name):
    """Отладочная функция для проверки состояния DOM"""
    print(f"\n=== DEBUG {step_name} ===")
    try:
        card_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Номер карты' or contains(@class, 'card') or @type='text']")
        print(f"Поля карты найдено: {len(card_inputs)}")
        for i, inp in enumerate(card_inputs):
            print(f"  Поле {i+1}: value='{inp.get_attribute('value')}', placeholder='{inp.get_attribute('placeholder')}'")
        
        amount_inputs = driver.find_elements(By.XPATH, "//input")
        print(f"Всего input полей: {len(amount_inputs)}")
        for i, inp in enumerate(amount_inputs):
            placeholder = inp.get_attribute('placeholder')
            value = inp.get_attribute('value')
            if placeholder and ('сумма' in placeholder.lower() or '1000' in placeholder):
                print(f"  Поле суммы {i+1}: value='{value}', placeholder='{placeholder}'")
        
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
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Всего кнопок найдено: {len(buttons)}")
        
        for i, btn in enumerate(buttons):
            text = btn.text
            class_name = btn.get_attribute("class")
            is_enabled = btn.is_enabled()
            is_displayed = btn.is_displayed()
            print(f"  Кнопка {i+1}: text='{text}', class='{class_name}', enabled={is_enabled}, displayed={is_displayed}")
            
            spans = btn.find_elements(By.TAG_NAME, "span")
            for j, span in enumerate(spans):
                span_text = span.text
                print(f"    Span {j+1}: text='{span_text}'")
        
        transfer_buttons = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ПЕРЕВЕСТИ', 'перевести'), 'перевести')]")
        print(f"Элементы с текстом 'перевести': {len(transfer_buttons)}")
        for elem in transfer_buttons:
            print(f"  Элемент: tag='{elem.tag_name}', text='{elem.text}'")
            
    except Exception as e:
        print(f"Ошибка при отладке кнопки: {e}")
    print("=== END DEBUG BUTTON ===\n")

def find_transfer_button(driver):
    """Находит кнопку 'Перевести' по тексту внутри span или по классу"""
    try:
        return driver.find_element(By.XPATH, "//button[.//span[contains(translate(text(), 'ПЕРЕВЕСТИ', 'перевести'), 'перевести')]]")
    except:
        pass
    try:
        return driver.find_element(By.XPATH, "//button[contains(@class, 'g-button') and contains(@class, 'outlined')]")
    except:
        pass
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
        
        alert_text = close_alert_if_present(driver)
        return alert_text
    except Exception as e:
        alert_text = close_alert_if_present(driver)
        if alert_text:
            return alert_text
        raise e