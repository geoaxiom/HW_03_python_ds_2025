import time
import schedule
import scraper


def scrape_job():
    print("scraper started")
    scraper.scrape_books()


schedule.every().day.at("19:45").do(scrape_job)

while True:
    schedule.run_pending()
    time.sleep(30)
