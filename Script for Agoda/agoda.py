from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pymysql
import os

#connect to mysql
db = pymysql.connect("localhost", "root", "", "reviewer")
cursor = db.cursor()

#open csv file
file = open(os.path.expanduser(r"~/Desktop/Agoda Reviews.csv"), "wb")
file.write(
    b"Review,Rating Date,Rating  " + b"\n")

#extract booking and insert to database
def agoda():
    browser = webdriver.Chrome()
    browser.get('https://www.agoda.com/taal-vista-hotel/hotel/tagaytay-ph.html')

    try:
        WebDriverWait(browser, 50).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-selenium='reviews-comments']")))
    except TimeoutException:
        print("Timed out! Waiting for page to load")
        browser.quit()

    count = 0
    agoda_id = 100
    while True:
        Review_element = browser.find_elements_by_xpath("//*[@data-selenium='reviews-comments']")
        Rating_date_element = browser.find_elements_by_xpath("//*[@data-selenium='review-date']")
        Rating_element = browser.find_elements_by_xpath("//*[@data-selenium='individual-review-rate']")

        Review = []
        Rating_date = []
        Rating = []

        for x in range(10):

            Review.append(Review_element[x].text.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').replace('\n', ' ').strip())
            Rating.append(Rating_element[x].text.replace('.','').strip())
            Rating_date.append(Rating_date_element[x].text.replace('Reviewed', ' ').replace('NEW',' ').replace(',', ' ').strip())

            #print at cmd
            print(Review[count] + Rating[count] + Rating_date[count])

            #insert to database (negative reviews)
            cursor.execute("INSERT INTO CUSTOMER  (REVIEWSITES_ID, CSTMR_REVIEW, CSTMR_RATINGDATE, CSTMR_RATING) values (%s,%s,%s,%s)",
            (agoda_id, str(Review[count]),str(Rating_date[count]),str(Rating[count])))

            db.commit()
            count = count + 1

            db.commit()
            count = count + 1

            if count == 5:
                break

            '''
            #write into csv file
            Record = Review[count] + "," + Rating_date[count] + "," + Rating[count]

            file.write(bytes(Record, encoding="ascii", errors='ignore')  + b"\n")
            '''
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
  agoda()
