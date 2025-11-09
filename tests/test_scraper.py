import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import scraper


def test_scrape_books():
    res = scraper.scrape_books(is_save=False)
    assert len(res) == 1000, "Список должен содержать 1000 словарей"


def test_get_catalogue_pages():
    catalogue_pages = scraper.get_catalogue_pages(scraper.BASE_CATALOGUE_PAGE_URL)
    assert len(catalogue_pages) == 50, "Должно быть 50 страниц каталога"


def test_get_books_links():
    links = scraper.get_books_links('https://books.toscrape.com/catalogue/page-{N}.html'.format(N=1))
    assert len(links) == 20, "На странице должно быть 20 ссылок на книги."


def test_get_book_data():
    """
    {"title": "The Story of Art",
     "price": "£41.14",
     "availability": "In stock (7 available)",
     "star_rating": "Four",
     "description": "This text is the 16th revised and updated edition of this
        introduction to art, from the earliest cave paintings to experimental art.
        Eight new artists from the modern period have been introduced. They are:
        Corot, Kollwitz, Nolde, de Chirico, Brancussi, Magritte, Nicolson and Morandi.
        A sequence of new endings have been added, and the captions are now fuller,
        including the This text is the 16th revised and updated edition of this
        introduction to art, from the earliest cave paintings to experimental art.
        Eight new artists from the modern period have been introduced.
        They are: Corot, Kollwitz, Nolde, de Chirico, Brancussi, Magritte,
        Nicolson and Morandi. A sequence of new endings have been added,
        and the captions are now fuller, including the medium and dimension
        of the works illustrated. Six fold-outs present selected large-scale works.
        They are: Van Eyck's Ghent Altarpiece, Leonardo's Last Supper,
        Botticelli's Birth of Venus, Jackson Pollock's One (Number 31, 1950),
        Van der Weyden's Descent from the Cross and Michelangelo's Sistine
        Chapel ceiling. ...more",
    "upc": "9147c5251cc99eb1",
    "product_type": "Books",
    "price_without_tax": "£41.14",
    "price_with_tax": "£41.14",
    "tax_rate": "£0.00",
    "reviews_number": "0"}
    """
    book_url = 'https://books.toscrape.com/catalogue/the-story-of-art_500/index.html'
    book_dict = scraper.get_book_data(book_url)
    assert book_dict['title'] == "The Story of Art", "Название должно быть The Story of Art."
    assert book_dict['upc'] == "9147c5251cc99eb1", "upc должно быть 9147c5251cc99eb1."
    assert len(book_dict) == 11, "В словаре должно быть 11 значений"


def test_get_response():
    correct_url = 'https://books.toscrape.com/catalogue/the-story-of-art_500/index.html'
    incorrect_url = 'https://books.toscrape.com/catalogue/the-wrong-story/index.html'
    response, status_code = scraper.get_response(correct_url)
    assert status_code == 200, "Код HTTP ответа должен быть 200."
    response, status_code = scraper.get_response(incorrect_url)
    assert status_code == 404, "Код HTTP ответа должен быть 404."
