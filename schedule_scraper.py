import time
import schedule
import scraper


def scrape_job():
    print(f"Парсинг стартовал в {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
    scraper.scrape_books()


schedule.every().day.at("19:00").do(scrape_job)

while True:
    schedule.run_pending()
    time.sleep(30)
