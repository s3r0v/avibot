import requests
import openpyxl
import time
from random import randint
import os
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def parse(links, name, available_nums):
    REGION_INFO = 'region_info'
    CATEGORIES_INFO = 'categories_info'
    AVITO_MAIN = 'avito_main'
    #available_nums = int(balance/11)
    sessids = file_to_array('sessid.txt')
    sessid = str(sessids[-1])
    numbers_flag = 0

    cookie = {"name":"sessid", "value":sessid}

    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "Mozilla/95.0.2 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3")
    options.set_preference('permissions.default.image', 2)
    options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    options.add_argument('--no-sandbox')
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://m.avito.ru")
    driver.add_cookie(cookie)
    nums = []
    links = links[:available_nums+1]

    for link in links:
        try:
            driver.get(link)
            #WebDriverWait(driver,10).until(EC.element_to_be_clickable(By.XPATH, "//button[@class='mav-vpko6w']")).click()
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='mav-vpko6w']"))).click()
            time.sleep(1)
            nums.append(driver.find_element_by_xpath("//span[@data-marker='phone-popup/phone-number']").text)

        except Exception as e:
            print(e)
            nums.append("-")

        for num in nums:
            if num != "-":
                numbers_flag+=1
    #delete_last_line('sessid.txt')
    return numbers_flag, nums
    

def file_to_array(file):
    arr = []
    with open(file) as f:
        while True:
            line = f.readline()
            if not line:
                break
            arr.append(line.strip())
    return arr

print(parse(['https://www.avito.ru/moskva/nastolnye_kompyutery/apple_imac_27_late_2013_16gb_1tb_2284467994'], "2131826670.953.xlsx", 1))