"""A test selenium example to craw good pictures"""

import sys
sys.path.append(
    r'F:/Code/JustFor_Practice/justfor_practice/just-for-test/src/selenium/')
from justPlay.util.util import find_element_safe, KEYWORD
from selenium.webdriver.common.by import By
from selenium import webdriver
import dateutil.parser as dparser
import datetime
import time

datefile_root_path = "F:/New Folder/新しいフォルダー (7)/aisinei/"
lib_for_search = "XIAOYU语画界"
save_path = ""
date_file = open(datefile_root_path + lib_for_search + "/date.txt", "r")
base_date = dparser.parse(date_file.read(), fuzzy=True)

# Optional argument, if not specified will search path.
driver = webdriver.Chrome(r'F:/Code/reference/chromedriver/chromedriver.exe')
driver.get('https://www.aisinei.net/')
# go to the targeted lib
target_button = driver.find_element(
    By.XPATH, "//td[contains(@class,'fl_g')]//a[contains(text(),'{}')]".format(lib_for_search))
target_button.click()

# time.sleep(1)
# new_window_button = driver.find_element(By.XPATH,
#   "//span[@id='atarget']")
# new_window_button.click()

time.sleep(1)
image_mode_button = driver.find_element(By.XPATH,
                                        "//a[@class='chked']")
if image_mode_button:
    image_mode_button.click()

while True:
    paging_box = find_element_safe(driver, By.XPATH, "//a[@class='nxt']")
    if paging_box:
        task_list = driver.find_elements(
            By.XPATH, "//div[@class='posttitle']//a[@class='st']")
        true_task_list = []
        for task in task_list:
            task_text = task.text
            task_date = dparser.parse(task_text, fuzzy=True).date()
            if task_date > base_date:
                true_task_list.append(task)
                print(task_text)

        if not true_task_list:
            break

        for task in true_task_list:
            print("Current Crawing {}".format(task_text))
            task.click()

            time.sleep(1)

            tabs = driver.window_handles
            print(tabs)
            driver.switch_to.window(tabs[1])

            describe_text = driver.find_element(
                By.XPATH, "//td[contains(@id,'postmessage')]")
            print(describe_text.text)

            desc_text = describe_text.text.split(
                "[套图简介]", 1)[1].split("[会员下载]", 1)[0]
            is_target = any(key_word in desc_text for key_word in KEYWORD)
            if is_target:
                big_pic_btn = driver.find_element(
                    By.XPATH, "//a[@class='xi2 attl_m']")
                big_pic_btn.click()

            time.sleep(3)
            driver.close()
            driver.switch_to.window(tabs[0])

            # time.sleep(1)
            # driver.back()

        paging_box.click()
        time.sleep(1)
    else:
        break


time.sleep(2)
driver.back()
# search_box.send_keys('ChromeDriver')
# search_box.submit()
time.sleep(5)  # Let the user actually see something!
driver.quit()
