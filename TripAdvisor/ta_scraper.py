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

file = open(os.path.expanduser(r"~/Desktop/TripAdviser2 Reviews.csv"), "wb")
file.write(
    b"Reviewer,Review Title,Review,Rating Date,Rating  " + b"\n")

def tripadvisor():
    browser = webdriver.Chrome()
    browser.get('https://www.tripadvisor.com.ph/Hotel_Review-g317121-d320846-Reviews-Taal_Vista_Hotel-Tagaytay_Cavite_Province_Calabarzon_Region_Luzon.html#REVIEWS')

    try:
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="taplc_location_reviews_list_hotels_0"]/div[12]/div')))
    except TimeoutException:
        print("Timed out! Waiting for page to load")
        browser.quit()


    moreButton = browser.find_element_by_css_selector("span.taLnk.ulBlueLinks")
    moreButton.click()

    try:
        WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="review_516865814"]/div/div[2]/div/div[1]/div[3]/div/p/span')))
    except TimeoutException:
        print("Timed out! Waiting for more button to load")
        browser.quit()

    count = 0
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    while True:
        Reviewer_element = browser.find_elements_by_xpath("//*[@class='expand_inline scrname']")
        Review_title_element = browser.find_elements_by_xpath("//*[@class='noQuotes']")
        Review_element = browser.find_elements_by_css_selector(".partial_entry:nth-child(1)")
        Rating_date_element = browser.find_elements_by_xpath("//*[@class='ratingDate relativeDate']")
        Rating_element = browser.find_elements_by_xpath("//*[@class='rating reviewItemInline']")

        Reviewer = []
        Review_title = []
        Review = []
        Rating_date = []
        Rating = []

        for x in range(5):

            Reviewer.append(Reviewer_element[x].text.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').strip())
            Review_title.append(Review_title_element[x].text.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').strip())
            Review.append(Review_element[x].text.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').replace('\n', ' ').strip())
            Rating_date.append(Rating_date_element[x].text.replace('Reviewed', ' ').replace('NEW',' ').replace(',', ' ').strip())

            for i in soup.findAll(attrs={"class": "rating reviewItemInline"}):

                if i.find(class_ = "ui_bubble_rating bubble_50"):
                    rate = str(100)
                    Rating.append(rate)
                elif i.find(class_ = "ui_bubble_rating bubble_40"):
                    rate = str(80)
                    Rating.append(rate)
                elif i.find(class_ = "ui_bubble_rating bubble_30"):
                    rate = str(60)
                    Rating.append(rate)
                elif i.find(class_ = "ui_bubble_rating bubble_20"):
                    rate = str(40)
                    Rating.append(rate)
                elif i.find(class_ = "ui_bubble_rating bubble_10"):
                    rate = str(20)
                    Rating.append(rate)

            print(Reviewer[count] + " : " + Review_title[count] + " : " + Review[count] + " : " + Rating_date[count] + " : " + Rating[count])
            count = count + 1

        count = 0
        link = soup.find_all(attrs={"class": "nav next taLnk "})
        if link == False:
            break

        else:
            try:
                WebDriverWait(browser, 200).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="taplc_location_reviews_list_hotels_0"]/div[12]/div')))
                NextButton = browser.find_element_by_css_selector("span.nav.next.taLnk ")
                NextButton.click()
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, "html.parser")

                try:
                    WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span.taLnk.ulBlueLinks")))
                except Exception:
                    print("Timed out! Waiting for page to load")
                    browser.quit()


                if WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#taplc_location_reviews_list_hotels_0"))):
                    WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span.taLnk.ulBlueLinks")))
                    morebutton = browser.find_element_by_css_selector("span.taLnk.ulBlueLinks")
                    morebutton.click()

                    try:
                        WebDriverWait(browser, 200).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="review_516865814"]/div/div[2]/div/div[1]/div[3]/div/p/span')))
                        WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".expand_inline.scrname")))
                        WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".noQuotes")))
                        WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".partial_entry")))
                        WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".ratingDate.relativeDate")))
                        WebDriverWait(browser, 200).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".rating.reviewItemInline")))
                    except Exception:
                        print("Timed out! Waiting for more button to load")
                        browser.quit()

            except Exception:
                print("Timed out! Waiting for next button to load")
                browser.quit()


if __name__ == "__main__":
  tripadvisor()
