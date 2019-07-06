
from selenium.common.exceptions import NoSuchElementException


def find_element_safe(driver, option, regex):
    try:
        return driver.find_element(option, regex)
    except NoSuchElementException:
        return None

KEYWORD = ["黑丝", "丝袜 "]