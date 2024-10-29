from backend.utils.scrappers import scrap_website_driver, scrap_website_soup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logger = logging.getLogger("__name__")

DEBUG = True


def btc_talk():
    today_lines = []
    with scrap_website_soup("https://bitcointalk.org/index.php?board=159.0") as soup:
        trs = soup.find_all("tr")
        for tr in trs:
            if "October 28" in tr.text:
                line = [td.text.strip() for td in tr.find_all("td")]
                today_lines.append(line)
    return today_lines


if __name__ == "__main__":
    todays = btc_talk()
    for today in todays:
        print(f"Subject: {today[2]}")
        print(f"Replies: {today[3]}")
        print(f"Views: {today[4]}")
        print(f"Last post: {today[6]}")
