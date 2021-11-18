from selenium.webdriver.common.by import By

# Selenium locators

ZIP_CODE = (By.XPATH, "//div[contains(@class, 'zip')]/input")
DISTANCE_SELECT = (By.XPATH, "//div[contains(@class, 'radius')]/select")
DISTANCE_OPTION = (By.XPATH, "//option[contains(text(), '{radius}')]")
CAR_LINK = (By.XPATH, "//div[contains(@class, 'card')]//a")
CAR_HEADER = (By.XPATH, "//div[contains(@class, 'vdp-top')]/h1")
CAR_PRICE = (By.XPATH, "//div[contains(@class, 'price-box')]/h2")
CAR_SUMMARY = (By.XPATH, "//th[contains(text(), 'Summary')]/../..")
CAR_OPTIONS = (By.ID, 'options-table')
TR = (By.TAG_NAME, 'tr')
TH = (By.TAG_NAME, 'th')
TD = (By.TAG_NAME, 'td')
