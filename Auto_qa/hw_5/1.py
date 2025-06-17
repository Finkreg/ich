import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/iframes.html")
    yield driver
    driver.quit()


def test_text_in_iframe(driver):
    wait = WebDriverWait(driver, 10)

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "my-iframe")))

    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "p")))
    paragraphs = driver.find_elements(By.TAG_NAME, "p")

    target_text = "semper posuere integer et senectus justo curabitur"
    found = False

    for paragraph in paragraphs:
        if target_text in paragraph.text:
            assert paragraph.is_displayed(), "Параграф найден, но не отображается"
            found = True
            break

    assert found, f"Текст '{target_text}' не найден ни в одном параграфе"
