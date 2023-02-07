import time
from datetime import datetime

import json
import csv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service

import mail_file
from main import linc
# import main

cur_time = datetime.now().strftime('%d_%m_%Y_%H_%M')

def get_source_html(linc):
    
    options = webdriver.ChromeOptions()
    options.add_argument(
        argument='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')

    s = Service(executable_path='/home/nikulin/chromedriver')

    driver = webdriver.Chrome(service=s, options=options)
    # driver.maximize_window()

    try:
        driver.get(linc)
        time.sleep(10)
        json_data = driver.page_source
        json_data = json_data.split('>')[6].split('<')[0]
        json_data = json.loads(json_data)
        get_result(json_data)

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()

def get_result(json_data):   
    with open(f'avito.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                'id',
                'Название',
                'Локация',
                'Цена',
                'Примечание',
                'Дата, время публикации',
                'Url'
            ]
        )
    
    for item in json_data['items']:
        title = item['title'].replace('&nbsp;', ' ')
        timestamp = datetime.fromtimestamp(item['sortTimeStamp'])
        timestamp = datetime.strftime(timestamp, '%d.%m.%Y в %H %M')
        url_off = 'https://www.avito.ru' + item['urlPath'].strip()

        with open(f'avito.csv', 'a', encoding="utf-8", newline='') as file:
            writer = csv.writer(file)

            writer.writerow(
                    [
                        item['id'],
                        title,
                        item['location']['name'],
                        item['priceDetailed']['value'],
                        item['priceDetailed']['postfix'],
                        timestamp,
                        url_off
                    ]
                )
        # mail_file.file_mail(email=email)
        

if __name__ == '__main__':
    get_source_html(linc)