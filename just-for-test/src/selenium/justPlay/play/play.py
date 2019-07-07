"""A test selenium example to craw good pictures"""

import sys
sys.path.append(
    r'F:/Code/JustFor_Practice/justfor_practice/just-for-test/src/selenium/')
from justPlay.util.util import find_element_safe, KEYWORD
from selenium.webdriver.common.by import By
from selenium import webdriver
import dateutil.parser as dparser
import time
import os
import requests

datefile_root_path = "F:/New Folder/新しいフォルダー (7)/aisinei/"
lib_for_search = "XIAOYU语画界"
save_path = ""
date_file = open(datefile_root_path + lib_for_search + "/date.txt", "r+")
base_date = dparser.parse(date_file.read(), fuzzy=True).date()
write_date = base_date
finished_tasks = []
problem_tasks = []

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
image_mode_button = find_element_safe(driver, By.XPATH,
                                      "//a[@class='chked']")
if image_mode_button:
    image_mode_button.click()

while True:
    task_list = driver.find_elements(
        By.XPATH, "//div[@class='posttitle']//a[@class='st']")
    true_task_list = []
    for task in task_list:
        task_text = task.text
        task_date = dparser.parse(task_text.split(" ")[1], fuzzy=True).date()
        if task_date > base_date:
            true_task_list.append(task)
            write_date = task_date
            print(task_text)

    if not true_task_list:
        break

    for task in true_task_list:
        task_text = task.text
        try:
            print("Current Crawing {}".format(task_text))
            task.click()

            tabs = driver.window_handles
            print(tabs)
            driver.switch_to.window(tabs[1])

            describe_text = driver.find_element(
                By.XPATH, "//td[contains(@id,'postmessage')]")
            # print(describe_text.text)

            desc_text = describe_text.text.split(
                "[套图简介]", 1)[1].split("[会员下载]", 1)[0]
            print(desc_text)
            is_target = any(key_word in desc_text for key_word in KEYWORD)
            print(is_target)
            if is_target:
                task_dir = datefile_root_path + lib_for_search + "/" + task_text
                if not os.path.exists(task_dir):
                    os.makedirs(task_dir)
                else:
                    print("duplicated")
                    continue
            else:
                continue
            big_pic_btn = driver.find_element(
                By.XPATH, "//a[@class='xi2 attl_m']")
            big_pic_btn.click()
            time.sleep(1)
            pictures = driver.find_elements(By.XPATH, "//img[contains(@id,'aimg_')]")
            folder_size = len(pictures)
            for index, pic in enumerate(pictures):
                pic_src = pic.get_attribute("src")
                print("downloading {}/{}".format(index + 1, folder_size))
                html = requests.get(pic_src, stream=True)
                with open("{}/{}.png".format(task_dir, index), "wb") as f:
                    f.write(html.content)
                time.sleep(0.5)
        except Exception:
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
date_file.seek(0)
date_file.write(write_date)
date_file.close()
driver.quit()
