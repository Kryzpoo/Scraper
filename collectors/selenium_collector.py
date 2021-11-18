from processors import BaseProcessor
from utils import locators, selenium_utils
from writers import BaseWriter
from .base import BaseCollector


class SeleniumCollector(BaseCollector):
    """
    Collector based on Selenium.
    The idea is in launching webdriver, setting search parameters
    and collecting links for cars.
    """

    def __init__(self, url: str, zip_code: str, radius: str,
                 processor: BaseProcessor, writer: BaseWriter):
        self.URL_MAIN_PAGE = f'{url}/buy?body_style=&distance=50&exterior_color_id=&make=&miles_max=100000&miles_min=0&model=&page_size=24&price_max=100000&price_min=0&query=&requestingPage=buy&sort=desc&sort_field=updated&status=active&year_end=2022&year_start=1998&zip='
        self.driver = None
        self.zip_code = zip_code
        self.radius = radius
        self.processor = processor
        self.writer = writer

    def start(self) -> None:
        self.driver = selenium_utils.start_webdriver()

    def stop(self) -> None:
        self.driver.close()

    def get_scroll_height(self) -> int:
        return self.driver.execute_script("return document.body.scrollHeight")

    def scroll_up(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_down(self) -> None:
        self.driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")

    def remove_cars_from_page(self) -> None:
        self.driver.execute_script(
            "document.querySelectorAll('.card').forEach(function(e) {e.remove();});")

    def collect(self) -> None:
        # Open page
        self.driver.get(self.URL_MAIN_PAGE)
        selenium_utils.webdriver_wait_for_presence(self.driver)

        # Insert zip code
        el_zip_code = self.driver.find_element(*locators.ZIP_CODE)
        el_zip_code.send_keys(self.zip_code)

        # Insert distance
        el_distance_select = self.driver.find_element(*locators.DISTANCE_SELECT)
        el_distance_select.click()
        el_distance = el_distance_select.find_element(
            locators.DISTANCE_OPTION[0],
            locators.DISTANCE_OPTION[1].format(radius=self.radius)
        )
        el_distance.click()

        # Wait filtering
        selenium_utils.webdriver_wait_for_presence(self.driver)

        # Since the page has pagination with additional loading
        # 1. Need to get current length of the page
        # 2. Then process objects
        # 3. Get new length of the page
        # 4. After processing objects are deleted
        # 5. Scroll up and down in order to trigger loading of new objects
        # After deleting objects new length is slightly more than previous
        # 6. Repeat 2-5 steps until length stops increasing

        # Step 1
        last_height = self.get_scroll_height()
        while True:
            self.scroll_up()

            # Wait to load page
            selenium_utils.webdriver_wait_for_presence(self.driver)

            # Step 2: get links, process them, write results
            el_car_links = [link.get_property('href') for link in
                            self.driver.find_elements(*locators.CAR_LINK)]
            results = self.processor.process(el_car_links)
            self.writer.write_many(results)

            # Step 3
            new_height = self.get_scroll_height()
            if new_height <= last_height:
                # Step 6
                break
            last_height = new_height

            # Step 4
            self.remove_cars_from_page()

            # Step 5
            self.scroll_up()
            self.scroll_down()
