import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

@pytest.fixture(scope="module")
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_button_text_change(driver):
    """
    Тест проверяет изменение текста кнопки после ввода текста в поле и клика.
    """
    url = "http://uitestingplayground.com/textinput"
    input_text = "ITCH"

    print(f"\n1. Переходим на сайт: {url}")
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # 2. Введите в поле ввода текст "ITCH".
    try:
        text_input_field = wait.until(EC.presence_of_element_located((By.ID, "newButtonName")))
        text_input_field.clear()
        text_input_field.send_keys(input_text)
        print(f"✅ Ввели текст '{input_text}' в поле ввода.")
    except Exception as e:
        pytest.fail(f"❌ Не удалось найти или ввести текст в поле ввода: {e}")

    # 3. Нажмите на синюю кнопку.
    try:
        blue_button = wait.until(EC.element_to_be_clickable((By.ID, "updatingButton")))
        initial_button_text = blue_button.text 
        print(f"Начальный текст кнопки: '{initial_button_text}'")
        blue_button.click()
        print("✅ Кликнули по синей кнопке.")
    except Exception as e:
        pytest.fail(f"❌ Не удалось найти или кликнуть по синей кнопке: {e}")

    # 4. Проверьте, что текст кнопки изменился на "ITCH".
    try:
        wait.until(EC.text_to_be_present_in_element((By.ID, "updatingButton"), input_text))
        final_button_text = driver.find_element(By.ID, "updatingButton").text
        assert final_button_text == input_text, f"❌ Текст кнопки не изменился на '{input_text}'. Текущий текст: '{final_button_text}'"
        print(f"✅ Текст кнопки успешно изменился на '{final_button_text}'") 
    except Exception as e:
        pytest.fail(f"❌ Текст кнопки не изменился на '{input_text}' или не был найден: {e}")