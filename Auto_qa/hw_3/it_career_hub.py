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

def test_itcareerhub_page_elements(driver):
    """
    Тест проверяет наличие основных элементов на главной странице ITCareerHub
    и функциональность иконки телефонной трубки.
    """
    driver.get("https://itcareerhub.de/ru")

    wait = WebDriverWait(driver, 10)

    print("\nПроверка наличия основных элементов на странице...")

    # 1. Проверка логотипа ITCareerHub
    try:
        logo = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div/div/div[11]/a/img")))
        assert logo.is_displayed(), "Логотип ITCareerHub не отображается."
        print("✅ Логотип ITCareerHub найден.")
    except Exception as e:
        pytest.fail(f"❌ Не удалось найти логотип ITCareerHub: {e}")

    # 2. Проверка наличия ссылок навигации
    nav_links = {
        "Программы": "/html/body/div[1]/div[5]/div/div/div[4]/a",
        "Способы оплаты": "/html/body/div[1]/div[5]/div/div/div[3]/a",
        "Новости": "/html/body/div[1]/div[5]/div/div/div[5]/a",
        "О нас": "/html/body/div[1]/div[5]/div/div/div[6]/a",
        "Отзывы": "/html/body/div[1]/div[5]/div/div/div[7]/a"
    }

    for link_text, xpath in nav_links.items():
        try:
            link = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            assert link.is_displayed(), f"Ссылка '{link_text}' не отображается."
            print(f"✅ Ссылка '{link_text}' найдена.")
        except Exception as e:
            pytest.fail(f"❌ Не удалось найти ссылку '{link_text}': {e}")

    # 3. Проверка кнопок переключения языка (ru и de)
    try:
        ru_lang_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div/div/div[9]/a")))
        assert ru_lang_button.is_displayed(), "Кнопка 'ru' не отображается."
        print("✅ Кнопка 'ru' найдена.")
    except Exception as e:
        pytest.fail(f"❌ Не удалось найти кнопку 'ru': {e}")

    try:
        de_lang_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div/div/div[10]/div/a")))
        assert de_lang_button.is_displayed(), "Кнопка 'de' не отображается."
        print("✅ Кнопка 'de' найдена.")
    except Exception as e:
        pytest.fail(f"❌ Не удалось найти кнопку 'de': {e}")

    print("\nПроверка функциональности иконки телефонной трубки...")

    # 4. Клик по иконке с телефонной трубкой
    try:
        phone_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[5]/div/div/div[13]/a/img")))
        phone_icon.click()
        print("✅ Клик по иконке телефонной трубки выполнен.")
    except Exception as e:
        pytest.fail(f"❌ Не удалось кликнуть по иконке телефонной трубки: {e}")

    # 5. Проверка текста "Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами"
    expected_text = "Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами"
    try:
        call_me_text_element = wait.until(EC.visibility_of_element_located((By.XPATH, f"/html/body/div[1]/div[7]/div/div[1]/div/div/div/div/div[6]/a")))
        assert call_me_text_element.is_displayed(), f"Текст '{expected_text}' не отображается."
        print(f"✅ Текст '{expected_text}' отображается.")
    except Exception as e:
        pytest.fail(f"❌ Не удалось найти или проверить текст '{expected_text}': {e}")