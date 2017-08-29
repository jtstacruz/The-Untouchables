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

file = open(os.path.expanduser(r"~/Desktop/Booking Reviews.csv"), "wb")
file.write(
    b"Review,Rating Date,Rating  " + b"\n")

def booking():
    browser = webdriver.Chrome()
    browser.get('https://www.booking.com/hotel/ph/taal-vista.en-gb.html#tab-reviews')

    try:
        WebDriverWait(browser, 50).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='review-policy__header-group']")))
    except TimeoutException:
        print("Timed out! Waiting for page to load")
        browser.quit()

    count = 0
    range_num = 11
    while True:
        Review_element_neg = browser.find_elements_by_xpath("//*[@class='review_neg']")
        Review_element_pos = browser.find_elements_by_xpath("//*[@class='review_pos']")
        Rating_date_element = browser.find_elements_by_xpath("//*[@class='review_item_date']")
        Rating_element = browser.find_elements_by_xpath("//*[@class='review-score-badge']")

        Review = []
        Review2 = []
        Rating_date = []
        Rating = []

        for x in range(range_num):

            Review.append(Review_element_neg[x].text.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').replace('\n', ' ').strip())
            Rating.append(Rating_element[x].text.replace('.','').strip())
            Rating_date.append(Rating_date_element[x].text.replace('Reviewed', ' ').replace('NEW',' ').replace(',', ' ').strip())

            print(Review[count] + Rating[count] + Rating_date[count])

            Review2.append(Review_element_pos[x].text.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').replace('\n', ' ').strip())

            print(Review2[count] + Rating[count] + Rating_date[count])

            '''
            if count == 5:
                break

            Record = Review[count] + "," + Rating_date[count] + "," + Rating[count]

            file.write(bytes(Record, encoding="ascii", errors='ignore')  + b"\n")
            '''
            count = count + 1
'''

        count = 0
        link = browser.find_elements_by_xpath("//*[@data-selenium='reviews-next-page-link']")
        if link == False:
            break
        else:
            try:
                WebDriverWait(browser, 200).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="next-page"]/i')))
                NextButton = browser.find_element_by_css_selector(".next-arrow")
                NextButton.click()

                try:
                    WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@data-selenium='reviews-comments']")))
                    WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@data-selenium='review-date']")))
                    WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@data-selenium='individual-review-rate']")))
                    WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@data-selenium='reviews-next-page-link']")))
                except Exception:
                    print("Timed out! Waiting for page to load")
                    browser.quit()

            except Exception:
                print("Timed out! Waiting for next button to load")
                browser.quit()
'''

if __name__ == "__main__":
  booking()
