from pathlib import Path
from typing import Tuple

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def start_webdriver(implicitly_wait: int = 10) -> WebDriver:
    # Choose driver binary
    drivers_dir = Path('drivers')
    drivers = [f for f in drivers_dir.iterdir()]
    driver_filename = None
    for d in drivers:
        if d.name.startswith('chrome'):
            driver_filename = str(d)

    # Here is place for extending drivers variety
    service = Service(driver_filename)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(implicitly_wait)

    return driver


def webdriver_wait_for_presence(driver: WebDriver,
                                locator: Tuple[By, str] = (
                                        By.XPATH,
                                        "//div[contains(@class, 'loader')]"
                                )) -> None:
    # Default wait
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except TimeoutException:
        pass


def find_element_safe(driver: WebDriver, by: By, locator: str) -> WebElement:
    # Safe wrap for `driver.find_element` method
    try:
        return driver.find_element(by, locator)
    except NoSuchElementException as e:
        pass
