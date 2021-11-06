# Парсинг категории (смартфоны)
import time
import uuid
from threading import Thread

import requests
from bs4 import BeautifulSoup
from .models import Products


def get_page(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    clean_url = url
    request = requests.get(url, headers)
    soup = BeautifulSoup(request.text, 'lxml')
    # pagination_div = soup.find('div', 'PaginationWidget__wrapper-pagination').text
    # print(pagination_div)
    page = soup.find('a', class_='PaginationWidget__page js--PaginationWidget__page PaginationWidget__page_last PaginationWidget__page-link').get('data-page')
    print(page)

    for x in range(1, (int(page) + 1), 1):
        url = f'{clean_url}?p={x}'
        print(f'Пожалуйса, подождите. Идет обработка данных {x} из {page}')
        request = requests.get(url, headers)
        soup = BeautifulSoup(request.text, 'lxml')

        item_div = soup.find_all("div",
                                 class_='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist')

        for x in item_div:
            try:
                price = x.find('span', class_='ProductCardHorizontal__price_current-price js--ProductCardHorizontal__'
                                              'price_current-price').text
            except:
                price = 0 # Товара нет в наличии, поэтому цена не известа. Помечаем как 0

            title_div = x.find('div', class_='ProductCardHorizontal__header-block')
            title = title_div.find('a').text
            photo_div = x.find('div', class_='ProductCardHorizontal__image-block')
            picture = photo_div.find('picture',
                                     class_='ProductCardHorizontal__picture js--ProductCardInListing__picture').find(
                'img').get('src')
            img = requests.get(picture).content
            name = uuid.uuid4()
            with open(f'media/parsing/{name}.jpg', 'wb') as file:
                file.write(img)
                file.close()
            try:
                price = price.replace(' ', '')
            except:
                pass
            product = Products.objects.create(title=title.replace(' ', ''), price=price,
                                              photo=f'media/parsing/{name}.jpg')

