import datetime
import json
import requests
from typing import Tuple
from bs4 import BeautifulSoup

BASE_CATALOGUE_URL = "https://books.toscrape.com/catalogue/"
BASE_CATALOGUE_PAGE_URL = "https://books.toscrape.com/catalogue/page-{N}.html"


def get_response(url: str) -> Tuple[requests.Response | None, int | None]:
    """
    Отправляет и получает ответ на GET запрос. Проверяет статусы ответов.

    Args:
        url: адрес страницы

    Returns:
        requests.Response в случае кода ответа 2хх
            None во всех остальных случаях
        Код HTTP ответа или None при requests.exceptions.RequestException

    Raises:
        requests.exceptions.RequestException: Ошибка HTTP запроса
            подобная ConnectionError, Timeout, HTTPError, SSLError итд.
    """
    status_code = None
    try:
        response = requests.get(url)
        if 200 <= response.status_code < 300:
            return response, response.status_code
        else:
            status_code = response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return None, status_code


def get_book_data(book_url: str) -> dict:
    """
    Собирает со страницы название книги, цену, рейтинг, количество в наличии,
    описание, характеристики из таблицы Product Information.

    Args:
        book_url: ссылка на страницу с информацией о книге.

    Returns:
        словарь с характеристиками книги
            title
            price
            availability
            star_rating
            description
            upc
            product_type
            price_without_tax
            price_with_tax
            tax_rate
            reviews_number
    """
    book_dict = {}
    response, status_code = get_response(book_url)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        product_page = soup.find('article', attrs={'class': 'product_page'})
        product_row = product_page.find('div', attrs={'class': 'row'})
        # title
        book_title = product_row.find('h1').text
        book_dict['title'] = book_title
        # price
        price = product_row.find('p', attrs={'class': 'price_color'}).text
        book_dict['price'] = price
        # availability
        availability = product_row.find('p', attrs={'class': 'instock availability'}).text.strip()
        book_dict['availability'] = availability
        # star-rating Four
        star_rating = product_row.find('p', attrs={'class': 'star-rating'})
        star_rating_class = star_rating.attrs['class']
        book_dict['star_rating'] = len(star_rating_class) == 2 and star_rating_class[1]
        # description
        product_description = product_page.find('div', id="product_description")
        book_dict['description'] = product_description and product_description.find_next_sibling('p').text
        # Product Information
        product_information = product_page.find('table', attrs={'class': "table table-striped"})
        table_ths = product_information.find_all('th')
        for th in table_ths:
            # upc
            if th.string == 'UPC':
                book_dict['upc'] = th.find_next_sibling('td').text
            # product_type
            elif th.string == 'Product Type':
                book_dict['product_type'] = th.find_next_sibling('td').text
            # price_without_tax
            elif th.string == 'Price (excl. tax)':
                book_dict['price_without_tax'] = th.find_next_sibling('td').text
            # price_with_tax
            elif th.string == 'Price (incl. tax)':
                book_dict['price_with_tax'] = th.find_next_sibling('td').text
            # tax_rate
            elif th.string == 'Tax':
                book_dict['tax_rate'] = th.find_next_sibling('td').text
            # reviews_number
            elif th.string == 'Number of reviews':
                book_dict['reviews_number'] = th.find_next_sibling('td').text
    else:
        print(f"Ошибка ответа от сервера. Код HTTP ответа: {status_code}")

    return book_dict


def get_books_links(url: str) -> list:
    """
    Собирает со страницы каталога ссылки на страницы с книгами.

    Args:
        url: ссылка на страницу каталога.

    Returns:
        Список ссылок на страницы с книгами
    """
    links = []
    response, status_code = get_response(url)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        ordered_list = soup.find('ol', attrs={'class': 'row'})
        h3_tags = ordered_list.find_all('h3')
        for h3 in h3_tags:
            links.append(h3.find('a')['href'])

    return links


def get_catalogue_pages(url: str) -> dict:
    """
    Собирает страницы каталога в словарь.

    Args:
        url: ссылка шаблон страницы каталога вида
            https://books.toscrape.com/catalogue/page-{N}.html

    Returns:
        Словарь со ссылками на все страницы каталога
        """
    catalogue_pages = {}
    page_num = 1
    while links := get_books_links(url.format(N=page_num)):
        catalogue_pages[page_num] = links
        page_num += 1

    return catalogue_pages


def runtime(func):
    """
    Декоратор для замера времени выполнения функции.
    """
    def runtime_wrapper(*args, **kwargs):
        start_datetime = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_datetime = datetime.datetime.now()
        time_difference = end_datetime - start_datetime
        total_seconds = time_difference.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Время работы: {int(hours):02}:{int(minutes):02}:{seconds:05.2f}")
        return result

    return runtime_wrapper


@runtime
def scrape_books(is_save: bool = True) -> list[dict]:
    """
    Собирает информацию о книгах на страницах каталога и в зависимости от
    настройки выводит результаты или в файл, или возвращает как результат работы

    Args:
        is_save: аргумент-флаг, который отвечает за сохранение результата
            в файл, если он будет равен `True`, то информация сохраняется
            построчно с конвертацией словаря в json
            в ту же папку в файл `books_data.txt`.


    Returns:
        Список ссылок на страницы с книгами
    """
    books = []

    for page, links in get_catalogue_pages(BASE_CATALOGUE_PAGE_URL).items():
        for link in links:
            book_dict = get_book_data(BASE_CATALOGUE_URL + link)
            books.append(book_dict)

    if is_save:
        with open('artifacts/books_data.txt', 'w', encoding='UTF-8') as file:
            for book in books:
                file.write(json.dumps(book, ensure_ascii=False) + '\n')

    return books

if __name__ == '__main__':
    res = scrape_books()
    print(type(res), len(res))  # и проверки
