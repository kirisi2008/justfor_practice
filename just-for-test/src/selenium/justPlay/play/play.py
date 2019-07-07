"""A test selenium example to craw good pictures"""

import sys
sys.path.append(
    r'F:/Code/JustFor_Practice/justfor_practice/just-for-test/src/selenium/')
from justPlay.util.util import find_element_safe, KEYWORD, str2bool
from selenium.webdriver.common.by import By
from selenium import webdriver
import dateutil.parser as dparser
import time
import os
import requests
import argparse
import traceback

datefile_root_path = "F:/New Folder/新しいフォルダー (7)/aisinei/"
LIB_FOR_SEARCH = "XIAOYU语画界"
save_path = ""
date_file = open(datefile_root_path + LIB_FOR_SEARCH + "/date.txt", "r+")
base_date = dparser.parse(date_file.read(), fuzzy=True).date()

finished_tasks = []
problem_tasks = []


def multiple_craw(driver, rules):
    """[summary]

    Args:
        driver ([type]): [description]

    Returns:
        [type]: [description]
    """
    task_list = driver.find_elements(
        By.XPATH, "//div[@class='posttitle']//a[@class='st']")

    true_task_list = []
    _write_date = ""

    for task in task_list:
        task_text = task.text
        if rules:
            no_on_task = task_text.split("No.")[1][:4].replace(' ', '')
            if no_on_task in rules:
                true_task_list.append(task)
        else:
            task_date = dparser.parse(task_text.split(" ")[1], fuzzy=True).date()
            if task_date > base_date:
                true_task_list.append(task)
                _write_date = task_date

    return true_task_list, _write_date


def main(lib_for_search, select_mode=False, list_mode=False, list_mode_lists=None):
    """[summary]

    Args:
        lib_for_search ([type]): [description]
        select_mode (bool, optional): [description]. Defaults to False.
        list_mode (bool, optional): [description]. Defaults to False.
        list_mode_lists ([type], optional): [description]. Defaults to None.
    """
    driver = webdriver.Chrome(r'F:/Code/reference/chromedriver/chromedriver.exe')
    if not select_mode:
        url = 'https://www.aisinei.net/'
        # Optional argument, if not specified will search path.
        driver.get(url)
        # go to the targeted lib
        target_button = driver.find_element(
            By.XPATH,
            "//td[contains(@class,'fl_g')]//a[contains(text(),'{}')]".format(lib_for_search))
        target_button.click()
        # time.sleep(1)
        # new_window_button = driver.find_element(By.XPATH,
        #   "//span[@id='atarget']")
        # new_window_button.click()

        time.sleep(1)
        image_mode_button = find_element_safe(driver, By.XPATH,
                                              "//a[@class='chked']")
        if image_mode_button:
            image_mode_button.click()

        while True:
            task_list, write_date = multiple_craw(driver, rules=sorted(
                list_mode_lists, reverse=True) if list_mode else None)
            for task in task_list:
                task_text = task.text
                try:
                    print("Current Crawing {}".format(task_text))
                    task.click()

                    tabs = driver.window_handles
                    driver.switch_to.window(tabs[1])
                    craw(driver, lib_for_search, select_mode=list_mode)
                except Exception:
                    traceback.print_exc()
                    print("{} failed.".format(task_text))
                    problem_tasks.append(task_text)
                finally:
                    driver.close()
                    driver.switch_to.window(tabs[0])
                    finished_tasks.append(task_text)

                time.sleep(1)

                # time.sleep(1)
                # driver.back()

            paging_box = find_element_safe(driver, By.XPATH, "//a[@class='nxt']")
            if paging_box:
                paging_box.click()
                time.sleep(1)
            else:
                break

        print(finished_tasks)
        print("finished")
        print("===============")
        if problem_tasks:
            print(problem_tasks)
            print("has problem")

        # search_box.send_keys('ChromeDriver')
        # search_box.submit()
        time.sleep(2)  # Let the user actually see something!
        if not list_mode:
            date_file.write(write_date.strftime("%Y.%m.%d"))
            date_file.close()
        driver.quit()

    elif select_mode:
        select_mode_urls = lib_for_search
        for url in select_mode_urls:
            print(url)
            driver.get(url)
            craw(driver, 'SINGLE', select_mode=select_mode)
            print("finished {}".format(url))
        print("all finished!")


def craw(page_driver, lib_for_search, select_mode=False):
    """[summary]

    Args:
        page_driver ([type]): [description]
        lib_for_search ([type]): [description]
        single (bool, optional): [description]. Defaults to False.
    """
    describe_text = page_driver.find_element(
        By.XPATH, "//td[contains(@id,'postmessage')]")

    task_text = page_driver.find_element(By.XPATH, "//span[@id='thread_subject']").text
    print(task_text)
    is_target = False
    if not select_mode:
        desc_text = describe_text.text.split(
            "[套图简介]", 1)[1].split("[会员下载]", 1)[0]
        is_target = any(key_word in desc_text for key_word in KEYWORD)
    if is_target or select_mode:
        task_dir = datefile_root_path + lib_for_search + "/" + task_text.replace('/', '_')
        if not os.path.exists(task_dir):
            os.makedirs(task_dir)
        else:
            print("duplicated")
            return
    else:
        print("不够刺激")
        return
    big_pic_btn = page_driver.find_element(
        By.XPATH, "//a[@class='xi2 attl_m']")
    big_pic_btn.click()
    time.sleep(1)
    pictures = page_driver.find_elements(By.XPATH, "//img[contains(@id,'aimg_')]")
    folder_size = len(pictures)
    for index, pic in enumerate(pictures):
        pic_src = pic.get_attribute("src")
        print("downloading {}/{}".format(index + 1, folder_size))
        html = requests.get(pic_src, stream=True)
        with open("{}/{}.png".format(task_dir, index), "wb") as f:
            f.write(html.content)
        time.sleep(0.35)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Say hello')
    parser.add_argument('lib', type=str, nargs='+',
                        help="lib to be craw")
    parser.add_argument('-l' '--list', type=str2bool, nargs='?',
                        const=True, default=False, dest="list_mode",
                        help="Activate nice mode.")
    parser.add_argument("--select", "-s", type=str2bool, nargs='?',
                        const=True, default=False, dest="select_mode",
                        help="Activate nice mode.")
    args = parser.parse_args()
    urls = args.lib
    if args.select_mode:
        main(urls, select_mode=args.select_mode)
    else:
        main(urls[0],
             select_mode=args.select_mode,
             list_mode=args.list_mode,
             list_mode_lists=urls[1:])
