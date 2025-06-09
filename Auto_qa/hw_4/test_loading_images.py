import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

@pytest.fixture(scope="module")
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_third_image_alt_attribute(driver):
    url = "https://bonigarcia.dev/selenium-webdriver-java/loading-images.html"
    expected_alt_value = "award"
    expected_image_count = 4

    try:
        driver.get(url)
    except Exception as e:
        pytest.fail(f"Не удалось загрузить страницу {url}: {e}")

    wait = WebDriverWait(driver, 25) 

    all_images = []
    try:
        wait.until(
            lambda d: len(d.find_elements(By.TAG_NAME, "img")) >= expected_image_count,
            message=f"Не удалось найти хотя бы {expected_image_count} изображений на странице."
        )
        all_images = driver.find_elements(By.TAG_NAME, "img")
    except Exception as e:
        pytest.fail(f"Проблема с ожиданием появления изображений в DOM: {e}")

    try:
        for i, img in enumerate(all_images):
            wait.until(
                lambda d, image=img: image.get_attribute("naturalWidth") is not None and \
                                     int(image.get_attribute("naturalWidth")) > 0 and \
                                     image.get_attribute("naturalHeight") is not None and \
                                     int(image.get_attribute("naturalHeight")) > 0,
                message=f"Изображение #{i+1} не загрузилось полностью за отведенное время."
            )
    except Exception as e:
        pytest.fail(f"Проблема с ожиданием полной загрузки изображений: {e}")

    if len(all_images) < expected_image_count:
        pytest.fail(f"После загрузки всех изображений, количество оказалось меньше {expected_image_count}: {len(all_images)}.")

    actual_alt_value = ""
    try:
        third_image_element = all_images[expected_image_count - 1]
        actual_alt_value = third_image_element.get_attribute("alt")
    except IndexError:
        pytest.fail(f"Список изображений пуст или содержит меньше {expected_image_count} элементов.")
    except Exception as e:
        pytest.fail(f"Не удалось получить атрибут 'alt' у третьего изображения: {e}")

    try:
        assert actual_alt_value == expected_alt_value, \
            f"Значение атрибута 'alt' не совпадает. Ожидалось: '{expected_alt_value}', Получено: '{actual_alt_value}'"
    except AssertionError as e:
        pytest.fail(e.args[0]) 