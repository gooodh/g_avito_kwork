
from datetime import datetime


import os
import pywebio
from pywebio.output import*
from pywebio.input import *
from pywebio.input import TEXT, FLOAT, select
from email_validator import validate_email, EmailNotValidError

import mail_file
import get_result_csv

location_reg=''
category=''
limit_req=0
linc=''

cur_time = datetime.now().strftime('%d_%m_%Y_%H_%M')
# @pywebio.config(theme='dark')
async def interfes():
    clear()
    logo_path = os.path.join('data', 'logo.jpg')
    put_image(open(logo_path, 'rb').read())
    location_reg = await select(
        'Вбарете регион',
        [
            'Barnaul',
            'alt-kray'

        ]
    )
    
    category = await select(
        'Вбарете Категорию',
        [
            'avto',
            'raznoe',
            'nedvizimost',
            'odejda, tovary_dlya_detey',
            'tovary_dlya_kompyutera',          
        ]
    )

    limit_req = await select(
            'Сколко последних обьявлений вы хотите получить',
            [
                '30',
                '40',
                '50',
                '60'
            ]
        )  
    
    global email
    email = await input("Ваш email:", type=TEXT)
    is_new_account = True # False for login pages

    try:
        validation = validate_email(email, check_deliverability=is_new_account)
        email = validation.email

    except EmailNotValidError as e:
        put_text(str(e))
        pass

    linc_address(location_reg, category, limit_req)
    put_text('Ваш файл сформирован')
    



def linc_address(location_reg, category, limit_req):

    locationid={'Barnaul': 621630,'alt-kray':621590}
    categoryid={'avto': 1, 'raznoe': 2, 'nedvizimost':4, 'odejda, tovary_dlya_detey_i_igrushki': 5, 'tovary_dlya_kompyutera': 6}
    loc=locationid[location_reg]
    cat=categoryid[category]

 
    linc = f'https://www.avito.ru/web/1/main/items?forceLocation=true&locationId={loc}&lastStamp=1675071341&limit={limit_req}&offset={limit_req}&categoryId={cat}'#alt-kray
    get_result_csv.get_source_html(linc=linc)
    mail_file.file_mail(email=email)
    


if __name__ == '__main__':
    
    pywebio.start_server(interfes, port='8000', debug=True)

