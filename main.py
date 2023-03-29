import time
import telebot
import requests
from bs4 import BeautifulSoup as bs

login_url = 'https://www.tesmanian.com/account/login?return_url=%2Faccount'
main_url = 'https://www.tesmanian.com'
chanel_id = ''
bot_api_key = ''

bot = telebot.TeleBot(token=bot_api_key)

data = {
        'username': username,
        'password': password
    }

tmp = []


def get_tesla_data():
    session = requests.Session()
    response = session.post(login_url, data=data)

    # Проверка успешности авторизации
    if response.status_code == 200:
        print('Успішно авторизовано')
        response = session.get(main_url)
        if response.status_code == 200:
            soup = bs(response.text, 'html.parser')
            items = soup.find_all('div', class_='blog-post-card__info')
            for item in items:
                link = item.find('a')['href']
                title = item.find('a').text
                if title not in tmp:
                    tmp.append(title)
                    bot.send_message(chat_id=chanel_id, text=f'{title}\nLink: {main_url + link}')
                    print(f'Publish new post')


    else:
        print('Помилка авторизаціїї')
        return


while True:
    try:
        get_tesla_data()
        time.sleep(15)
    except:
        continue
