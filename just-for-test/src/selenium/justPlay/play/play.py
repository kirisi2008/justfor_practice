import sys 
sys.path.append (r'F:/Code/JustFor_Practice/justfor_practice/just-for-test/src/selenium/') 

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from justPlay.util.util import find_element_safe, KEYWORD

lib_for_search = "XIAOYU语画界"

driver = webdriver.Chrome(r'F:/Code/reference/chromedriver/chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://www.aisinei.net/')
time.sleep(1) # Let the user actually see something!
# go to the 
target_button = driver.find_element(By.XPATH, 
  "//td[contains(@class,'fl_g')]//a[contains(text(),'{}')]".format(lib_for_search))
target_button.click()

time.sleep(1)
new_window_button = driver.find_element(By.XPATH, 
  "//span[@id='atarget']")
new_window_button.click()

time.sleep(1)
image_mode_button = driver.find_element(By.XPATH, 
 "//a[@class='chked']")
if image_mode_button:
    image_mode_button.click()

while True:
    paging_box = find_element_safe(driver, By.XPATH, "//a[@class='nxt']")
    if paging_box:
        task_list = driver.find_elements(By.XPATH, "//div[@class='posttitle']//a[@class='st']")

        for task in task_list:
            folder_name = task.text
            print("Current Crawing {}".format(folder_name))
            task.click()

            time.sleep(1)

            describe_text = driver.find_element(By.XPATH, "//td[contains(@id,'postmessage')]")
            print(describe_text.text)

            desc_text = describe_text.text.split("[套图简介]",1)[1].split("[会员下载]",1)[0]
            is_target = any(key_word in desc_text for key_word in KEYWORD)
            if (is_target):
              big_pic_btn = driver.find_element(By.XPATH, "//a[@class='xi2 attl_m']")
              big_pic_btn.click()

            time.sleep(3)
            driver.back()

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
time.sleep(5) # Let the user actually see something!
driver.quit()


