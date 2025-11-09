
### Структура файла репозиторя

* Файл `scraper.py` с рабочим кодом парсера.
* `README.md` с описанием проекта и инструкцией по запуску.
* Папка `artifacts/` с результатом сбора данных (`.txt` файл).
* Папка `tests/` с тестами на `pytest`.
* Папка `notebooks/` с заполненным ноутбуком `HW_03_python_ds_2025.ipynb`.
* Pull Request с комментарием из ветки `hw-books-parser` в ветку `main`.
* Примерная структура:

  ```
  books_scraper/
  ├── artifacts/
  │   └── books_data.txt
  ├── notebooks/
  │   └── HW_03_python_ds_2025.ipynb
  ├── scraper.py
  ├── README.md
  ├── tests/
  │   └── test_scraper.py
  ├── .gitignore
  └── requirements.txt
  ```
