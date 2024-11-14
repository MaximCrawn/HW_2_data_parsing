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
        try:
            name_info = book.find('h3').findChildren()[0]
            book_info['name'] = name_info.get('title', 'N/A')
            book_info['url'] = url + "/" + name_info.get('href', '')
        except AttributeError:
            book_info['name'] = 'N/A'
            book_info['url'] = 'N/A'
        
        price = book.find('p', {'class': 'price_color'})
        book_info['price'] = price.get_text().replace('Â', '') if price else 'N/A'
        
        availability = book.find('p', {'class': 'instock availability'})
        book_info['availability'] = availability.get_text(strip=True) if availability else 'N/A'

        all_books.append(book_info)

    print(f'\rProcessed page {page}', end='')
    page += 1

df = pd.DataFrame(all_books)

df.to_csv('books.csv', index=False, encoding='utf-8')

print("\nДанные сохранены в файл books.csv")
pprint(df.head())

