from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

browser = webdriver.Chrome()
browser.get('https://www.tripadvisor.com.ph/Hotel_Review-g317121-d320846-Reviews-Taal_Vista_Hotel-Tagaytay_Cavite_Province_Calabarzon_Region_Luzon.html#REVIEWS')

timeout = 10
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="taplc_location_reviews_list_hotels_0"]/div[12]/div')))
except TimeoutException:
    print("Time out! Waiting for page to load")
    browser.quit()


moreButton = browser.find_element_by_css_selector("span.taLnk.ulBlueLinks")
moreButton.click()


timeout = 10
try:
    WebDriverWait(browser, timeout).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="review_516865814"]/div/div[2]/div/div[1]/div[3]/div/p/span')))
except TimeoutException:
    print("Time out! Waiting for more button to load")
    browser.quit()
