from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import urllib
import os
import re
from urllib.request import urlopen

file = open(os.path.expanduser(r"~/Desktop/Agoda Reviews.csv"), "wb")
file.write(
    b"Review,Rating Date,Rating  " + b"\n")

def agoda():
    browser = webdriver.Chrome()
    browser.get('https://www.agoda.com/taal-vista-hotel/hotel/tagaytay-ph.html')

    try:
        WebDriverWait(browser, 50).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-selenium='reviews-comments']")))
    except TimeoutException:
        print("Timed out! Waiting for page to load")
        browser.quit()

    count = 0

    while True:
        Review_element = browser.find_elements_by_xpath("//*[@data-selenium='reviews-comments']")
        Rating_date_element = browser.find_elements_by_xpath("//*[@data-selenium='review-date']")
        Rating_element = browser.find_elements_by_xpath("//*[@data-selenium='individual-review-rate']")

        Review = []
        Rating_date = []
        Rating = []

        for x in range(4):

            Review.append(Review_element[x].text.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').replace('\n', ' ').strip())
            Rating.append(Rating_element[x].text)
            Rating_date.append(Rating_date_element[x].text.replace('Reviewed', ' ').replace('NEW',' ').replace(',', ' ').strip())


            print(Review[count] + Rating[count] + Rating_date[count])

            count = count + 1

            if count == 4:
                break

"""
            Record = Review[count] + "," + Rating_date[count] + "," + Rating[count]

            file.write(bytes(Record, encoding="ascii", errors='ignore')  + b"\n")

            count = count + 1

        count = 0
        link = browser.find_elements_by_xpath("//*[@class='ficon ficon-24 ficon-carrouselarrow-right']")
        if link == False:
            break

        else:
            try:
                WebDriverWait(browser, 200).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="next-page"]/i')))
                NextButton = browser.find_element_by_css_selector("span.nav.next.taLnk ")
                NextButton.click()

                #try:
                #    WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".expand_inline.scrname")))
                #    WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".noQuotes")))
                #    WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".partial_entry")))
                #    WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ratingDate.relativeDate")))
                #except Exception:
                #    print("Timed out! Waiting for page to load")
                #    browser.quit()

            except Exception:
                print("Timed out! Waiting for next button to load")
                browser.quit()
"""

if __name__ == "__main__":
  agoda()
