"""util functions for the selenium example
"""
from selenium.common.exceptions import NoSuchElementException
import argparse


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


def str2bool(v):
    """[summary]

    Args:
        v ([type]): [description]

    Raises:
        argparse.ArgumentTypeError: [description]

    Returns:
        [type]: [description]
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


KEYWORD = ["黑丝", "丝袜", "吊袜", "旗袍"]
