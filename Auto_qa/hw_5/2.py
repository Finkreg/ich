import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.globalsqa.com/demo-site/draganddrop/")

    try:
        consent_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent"))
        )
        consent_btn.click()
    except TimeoutException:
        print("Cookie-баннер не появился")

    yield driver
    driver.quit()


def test_drag_and_drop_image(driver):
    wait = WebDriverWait(driver, 10)

    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.demo-frame")))
    driver.switch_to.frame(iframe)

    gallery_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#gallery > li")))
    source_image = gallery_items[0]

    trash_area = driver.find_element(By.ID, "trash")

    ActionChains(driver).click_and_hold(source_image).move_to_element(trash_area).release().perform()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#trash > ul > li")))
    trash_images = driver.find_elements(By.CSS_SELECTOR, "#trash > ul > li")
    remaining_gallery = driver.find_elements(By.CSS_SELECTOR, "#gallery > li")

    assert len(trash_images) == 1, "В корзине должно быть одно изображение"
    assert len(remaining_gallery) == 3, "В галерее должно остаться три изображения"
