"""util functions for the selenium example
"""
from selenium.common.exceptions import NoSuchElementException


def find_element_safe(driver, option, regex):
    """safely search for elements.

    Returns:
        [webdriver.element]: [found element]
        [null]: [no result]
    """
    try:
        return driver.find_element(option, regex)
    except NoSuchElementException:
        return None


KEYWORD = ["黑丝", "丝袜 "]
