import logging
import re
from queue import Queue
from typing import Tuple

from utils import locators
from utils import selenium_utils
from .base import BaseProcessor

log = logging.getLogger('scraper')
PATTERN_NAME_1 = re.compile(r"\w's (.*) For Sale")
PATTERN_NAME_2 = re.compile(r"(.*) For Sale")


class SeleniumProcessor(BaseProcessor):
    """
    Processor based on Selenium.
    The idea is in launching some of webdriver instances
    and receiving data directly from pages.
    """

    def __init__(self, max_workers: int):
        self.MAX_WORKERS = max_workers
        self.free_drivers = None

    def start(self) -> None:
        # Since launch of webdriver is expensive
        # use a certain amount of instances
        self.free_drivers = Queue(self.MAX_WORKERS)
        for driver in range(self.MAX_WORKERS):
            # Use implicitly_wait = 0 since the page is static
            self.free_drivers.put(selenium_utils.start_webdriver(0))

    def stop(self) -> None:
        # Closing webdriver instances
        while True:
            if self.free_drivers.empty():
                break
            else:
                driver = self.free_drivers.get()
                driver.close()

    def get_data_one(self, link: str) -> Tuple[str, str, dict, list]:
        # Receive free driver
        driver = self.free_drivers.get()
        name = ''
        price = ''
        summary = {}
        options = []
        try:
            # Wait only once for page loading
            driver.get(link)
            selenium_utils.webdriver_wait_for_presence(driver, locators.CAR_HEADER)

            # Get name
            el_header = driver.find_element(*locators.CAR_HEADER)
            for pattern in (PATTERN_NAME_1, PATTERN_NAME_2):
                match = pattern.search(el_header.accessible_name)
                if match:
                    name = match.group(1)
                    break

            # Get price
            el_price = selenium_utils.find_element_safe(driver, *locators.CAR_PRICE)
            price = el_price.accessible_name if el_price else 'SOLD'

            # Get summary
            el_summary = driver.find_element(*locators.CAR_SUMMARY)
            for el in el_summary.find_elements(*locators.TR)[1:]:
                s_name = el.find_element(*locators.TH).accessible_name[:-1]
                s_value = el.find_element(*locators.TD).accessible_name
                summary[s_name] = s_value

            # Get options
            el_options = selenium_utils.find_element_safe(driver, *locators.CAR_OPTIONS)
            if el_options:
                opt_write = False
                for el in el_options.find_elements(*locators.TR):
                    if not opt_write and el.text == 'Options':
                        opt_write = True
                        continue
                    if opt_write:
                        options.append(el.text)
        except Exception:
            log.error(f'Error in processing link {link}', exc_info=True)
        finally:
            # Driver allocation
            self.free_drivers.put(driver)
        return name, price, summary, options
