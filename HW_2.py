#http://books.toscrape.com/
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint


ua = UserAgent()

url = 'https://books.toscrape.com/catalogue'
headers = {"User-Agent": ua.random}
page = 1

session = requests.Session()

all_books = []

while True:
    response = session.get(f"{url}/page-{page}.html", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all('article', {'class':'product_pod'})
    if not books:
        break    

    for book in books:
        book_info = {}
        name_info = book.find('h3').findChildren()[0]
        book_info['name'] = name_info.get('title')
        book_info['url'] = url + "/" + name_info.get('href')
        book_info['price'] = book.find('p', {'class': 'price_color'}).get_text().replace('Â', '')
        book_info['availability'] = book.find('p', {'class': 'instock availability'}).get_text(strip=True)
        


        all_books.append(book_info)

    # Обновляем строку в консоли (перезаписываем номер страницы)
    print(f'\rОбработана {page} страница', end='')
    page += 1

# pprint(all_books)
df = pd.DataFrame(all_books)

# Сохраняем DataFrame в CSV файл
df.to_csv('books.csv', index=False, encoding='utf-8')

# Выводим DataFrame для проверки
print("\nДанные сохранены в файл books.csv")
pprint(df.head())
