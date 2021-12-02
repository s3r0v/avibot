import requests
import openpyxl
import time
from random import randint
import os
import base64

def parse(links, name):
    REGION_INFO = 'region_info'
    CATEGORIES_INFO = 'categories_info'
    AVITO_MAIN = 'avito_main'
    #available_nums = int(balance/11)
    proxy_flag = 0
    sessids = file_to_array('sessid.txt')
    proxies = file_to_array('proxies.txt')
    sessid = str(sessids[-1])
    cookie = f'sessid={sessid};'
    s = requests.Session()                          # Будем всё делать в рамках одной сессии
    headers = { 'authority': 'm.avito.ru',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'ru-RU,ru;q=0.9',}
    if cookie:                                      # Добавим куки, если есть внешние куки
        headers['cookie'] = cookie
    s.headers.update(headers)                       # Сохраняем заголовки в сессию
    nums = []
    #links = links[:available_nums+1]
    for link in links:
        time.sleep(1)
        add_id = int(link.split("_")[-1])
        try:
            num = base64.decodestring(s.get(f'https://www.avito.ru/web/1/items/phone/{add_id}?vsrc=r&retina=1').json()['image64'].replace("data:image/png;base64,", "").replace("\"",""))
            num_pic = open(f'{name}.png', 'wb') # create a writable image and write the decoding result
            num_pic.write(num)
            if num[-11:]!="uthenticate":
                nums.append(num[-11:])
            else:
                while num[-11:]=="uthenticate":
                    delete_last_line('sessid.txt')
                    sessid = str(sessids[-1])
                    cookie = f'sessid={sessid};'
                    s = requests.Session()                          # Будем всё делать в рамках одной сессии
                    headers = { 'authority': 'm.avito.ru',
                                'pragma': 'no-cache',
                                'cache-control': 'no-cache',
                                'upgrade-insecure-requests': '1',
                                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36',
                                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                                'sec-fetch-site': 'none',
                                'sec-fetch-mode': 'navigate',
                                'sec-fetch-user': '?1',
                                'sec-fetch-dest': 'document',
                                'accept-language': 'ru-RU,ru;q=0.9',}
                    if cookie:                                      # Добавим куки, если есть внешние куки
                        headers['cookie'] = cookie
                    s.headers.update(headers)                       # Сохраняем заголовки в сессию
                    num = base64.decodestring(s.get(f'https://www.avito.ru/web/1/items/phone/{add_id}?vsrc=r&retina=1').json()['image64'].replace("data:image/png;base64,", "").replace("\"",""))
                    num_pic = open(f'{name}.png', 'wb') # create a writable image and write the decoding result
                    num_pic.write(num)
        except Exception:
            nums.append("-")
    numbers = 0
    for i in range(len(nums)):
        if nums[i]!="-":
            numbers += 1
    os.remove(name)
    #delete_last_line('sessid.txt')
    array_to_file(nums, name, numbers)
    

def handle_excel(file):
    wb = openpyxl.load_workbook(filename = file)
    ws = wb.active
    links = []

    columns = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for col in ws.iter_cols():
        for cell in col:
            if "Ссылка" in str(cell.value):
                column=cell.column
    for cell in ws[columns[column-1]]:
        if cell.value!=None:
            links.append(cell.value)
    return links[1:]

def file_to_array(file):
    arr = []
    with open(file) as f:
        while True:
            line = f.readline()
            if not line:
                break
            arr.append(line.strip())
    return arr

def delete_last_line(file):
    with open(file, "r+", encoding = "utf-8") as file:

        file.seek(0, os.SEEK_END)

        pos = file.tell() - 1

        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()

def array_to_file(nums, name, numbers):
    wb = openpyxl.load_workbook(name)
    sheets = wb.sheetnames
    sheet = wb[sheets[0]]
    f = 0

    for row in sheet:
        if f == 0:
            numbers = row[-1].offset(column=1)
            numbers.value = "Номера"
        else:
            numbers = row[-1].offset(column=1)
            try:
                numbers.value = nums[f-1]
            except Exception:
                numbers.value = "-"
        f+=1
    wb.save(name)
    return name, numbers

def connect_proxy(proxy_flag):
    proxy = file_to_array("proxies.txt")[proxy_flag].replace("@", ":").split(":")
    proxies = {'https':f'https://{proxy[0]}:{proxy[1]}@{proxy[2]}:{proxy[3]}'}
    return proxies