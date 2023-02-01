import time
from datetime import datetime
import json
import csv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service


import os
import pywebio
from pywebio.output import*
import pywebio.input as inp


location_reg=''
category=''
limit_req=0

cur_time = datetime.now().strftime('%d_%m_%Y_%H_%M')
@pywebio.config(theme='dark')
async def interfes():
    clear()
    logo_path = os.path.join('data', 'logo.jpg')
    put_image(open(logo_path, 'rb').read())
    location_reg = await inp.select(
        'Выберите нужный вариант',
        [
            'Вбарете регион',
            'Barnaul',
            'alt-kray'

        ]
    )
    
    category = await inp.select(
        'Выберите нужный вариант',
        [
            'Вбарете Категорию',
            'avto',
            'nedvizimost'

        ]
    )

    limit_req = await inp.select(
            'Выберите нужный вариант',
            [
                'Сколко последних обьявлений вы хотите получить',
                '30',
                '40',
                '50',
                '60'


            ]
        )
    linc_address(location_reg, category, limit_req)
    put_text('Ваш файл сформирован')

def get_source_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument(
        argument='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')

    s = Service(executable_path='/home/nikulin/chromedriver')

    driver = webdriver.Chrome(service=s, options=options)
    # driver.maximize_window()

    try:
        driver.get(url=url)
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

def linc_address(location_reg, category, limit_req):
    locationid={'Barnaul': 621630,'alt-kray':621590}
    categoryid={'avto': 1,'nedvizimost':4}
    # limit_req = int(limit_req)
    # print(limit_req)
    loc=locationid[location_reg]
    cat=categoryid[category]

    #
    # url = 'https://www.avito.ru/web/1/main/items?forceLocation=true&locationId=621590&lastStamp=1675071341&limit=30&offset=28&categoryId=1'#alt-kray
    url2 = f'https://www.avito.ru/web/1/main/items?forceLocation=true&locationId={loc}&lastStamp=1675071341&limit={limit_req}&offset={limit_req}&categoryId={cat}'#alt-kray
    get_source_html(url2)
    

def get_result(json_data):
    # with open('data.json', 'r', encoding='utf-8') as file:
    #     json_data = json.load(file)

    with open(f'avito{cur_time}.csv', 'w', encoding='utf-8', newline='') as file:
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

        with open(f'avito{cur_time}.csv', 'a', encoding="utf-8", newline='') as file:
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
if __name__ == '__main__':
    # url = 'https://www.avito.ru/web/1/main/items?forceLocation=false&locationId=621630&lastStamp=1672027185&limit=30&offset=54&categoryId=4'
    # url = 'https://www.avito.ru/web/1/main/items?forceLocation=false&locationId=621630&lastStamp=1672041950&limit=30&offset=29&categoryId=5'
    # url = 'https://www.avito.ru/web/1/main/items?forceLocation=false&locationId=621540&lastStamp=1675070512&limit=30&offset=60&categoryId=4'
    # url = 'https://www.avito.ru/web/1/main/items?forceLocation=true&locationId=621630&lastStamp=1675070788&limit=50&offset=50&categoryId=4'#barnaul
    # url = 'https://www.avito.ru/web/1/main/items?forceLocation=true&locationId=621590&lastStamp=1675071341&limit=30&offset=28&categoryId=1'#alt-kray

    # get_source_html(url)
    # interfes()
    pywebio.start_server(interfes, port='8000', debug=True)
    # get_source_html(url)
   
