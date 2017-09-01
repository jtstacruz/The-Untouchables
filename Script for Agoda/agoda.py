from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pymysql
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
#connect to mysql
db = pymysql.connect("localhost", "root", "", "reviewer")
cursor = db.cursor()

#open csv file
file = open(os.path.expanduser(r"~/Desktop/Agoda Reviews.csv"), "wb")
file.write(
    b"Review,Rating Date,Rating  " + b"\n")

#extract agoda and insert to database
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
        #######################################
        ####### EXTRACT DATA FROM AGODA #######
        #######################################
        Review_element = browser.find_elements_by_xpath("//*[@data-selenium='reviews-comments']")
        Rating_date_element = browser.find_elements_by_xpath("//*[@data-selenium='review-date']")
        Rating_element = browser.find_elements_by_xpath("//*[@data-selenium='individual-review-rate']")

        Review = []
        Rating_date = []
        Rating = []

        for x in range(5):
            if count == 5:
                browser.quit()

            Review.append(Review_element[x].text.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').replace('\n', ' ').strip())
            Rating.append(Rating_element[x].text.replace('.','').strip())
            Rating_date.append(Rating_date_element[x].text.replace('Reviewed', ' ').replace('NEW',' ').replace(',', ' ').strip())

            #print at cmd
            print(Review[count] + Rating[count] + Rating_date[count])

            ################################
            ###### INSERT TO DATABASE ######
            ################################
            cursor.execute("INSERT INTO CUSTOMER  (REVIEWSITES_ID, CSTMR_REVIEW, CSTMR_RATINGDATE, CSTMR_RATING) values (%s,%s,%s,%s)",
            (agoda_id, str(Review[count]),str(Rating_date[count]),str(Rating[count])))

            db.commit()

            ###########################
            ###### PREPROCESSING ######
            ###########################
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"         # emoticons
                u"\U0001F300-\U0001F5FF"         # symbols & pictographs
                u"\U0001F680-\U0001F6FF"         # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"         # flags (iOS)
                           "]+", flags=re.UNICODE)
            rx = re.compile('\W+')
            stop_words = set(stopwords.words("english"))


            first = emoji_pattern.sub(r'', Review[count])   #replace all emoji to blank space
            second = re.sub(r"http\S+", "", first)          #replace URL into blank space
            third = rx.sub(' ', second).strip()             #replace all non-alphanumerics to spaces
            words = word_tokenize(third.lower())            #tokenize and lower case
            filtered_sentence = []

            for w in words:
              if w not in stop_words:
                  filtered_sentence.append(w)
            print ("*************************************")
            print ("**********  CLEANED DATA  ***********")
            print ("*************************************")
            print ("*************************************")
            print ("".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in filtered_sentence]).strip())



            #############################################
            ###### INSERT TO DATABASE PREPROCESSED ######
            #############################################
            cursor.execute("INSERT INTO  PREPROCESSED(PREPROCESSED_REVIEW) values (%s)", (str(Review[count])))
            #commit insert
            db.commit()

            ###############################
            ###### COUNT OCCURENECE  ######
            ###############################
            words_pos = ["clean", "rooms", "amazing", "worth", "great", "luxury", "kind", "yummy", "better", "comfortable"]
            words_neg = ["old", "No", "horrible", "smelly", "failed", "disgusting", "poor", "not", "stains", "outdated", "noisy", "although" ]
            pos = 0
            neg = 0

            for word in Review[count]:
            	words.append(word)

            for item in words:
            	if item in words_pos:
            		pos += 1

            for item in words:
            	if item in words_neg:
            		neg += 1


            if pos > neg:
            	print("POSITIVE!" + " : " + str(pos))
            elif neg > pos:
            	print("NEGATIVE" + " : " + str(neg))
            elif neg == pos:
                print("NEUTRAL")

            print ("*************************************")
            print ("*************************************")
            count = count + 1

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
