# tripadvisor Scrapper - use this one to scrape hotels

# importing libraries
from bs4 import BeautifulSoup
import urllib
import os
import re
from urllib.request import urlopen

# creating CSV file to be used

file = open(os.path.expanduser(r"~/Desktop/Booking Reviews.csv"), "wb")
file.write(
    b"Organization,Address,Reviewer,Review Title,Review,Rating Date,Rating" + b"\n")

# List the first page of the reviews (ends with "#tab-reviews") - separate the websites with ,
WebSites = [
    "https://www.booking.com/hotel/ph/taal-vista.en-gb.html#tab-reviews"]
Checker = "REVIEWS"

# looping through each site until it hits a break
num = 0
for theurl in WebSites:
    thepage = urlopen(theurl)
    soup = BeautifulSoup(thepage, "html.parser")
    while True:
        # extract the help count, restaurant review count, attraction review count and hotel review count
        a = b = 0
        helpcountarray = restaurantarray = attractionarray = hotelarray = ""
        WebSites1 = ""

        for profile in soup.findAll(attrs={"class": "review_item_reviewer"}):
            image = profile.text.replace("\n", "|||||").strip()
            if image.find("restaurant") > 0:
                counter = image.split("restaurant", 1)[0].split("|", 1)[1][-4:].replace("|", "").strip()
                if len(restaurantarray) == 0:
                    restaurantarray = [counter]
                else:
                    restaurantarray.append(counter)
            elif image.find("restaurant") < 0:
                if len(restaurantarray) == 0:
                    restaurantarray = ["0"]
                else:
                    restaurantarray.append("0")

            if image.find("hotel") > 0:
                counter = image.split("hotel", 1)[0].split("|", 1)[1][-4:].replace("|", "").strip()
                if len(hotelarray) == 0:
                    hotelarray = [counter]
                else:
                    hotelarray.append(counter)
            elif image.find("hotel") < 0:
                if len(hotelarray) == 0:
                    hotelarray = ["0"]
                else:
                    hotelarray.append("0")

        Organization = soup.find(attrs={"class": "heading_title"}).text.replace('"', ' ').replace('Review of',
                                                                                                 ' ').strip()
        Address = soup.findAll(attrs={"class": "locality"})[0].text.replace(',', '').replace('\n', '').strip()

        # Loop through each review on the page
        for x in range(0, len(hotelarray)):
            try:
                Reviewer = soup.findAll(attrs={"class": "review_item_reviewer"})[x].text
            except:
                Reviewer = "N/A"
                continue

            Reviewer = Reviewer.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').strip()
            ReviewTitle = soup.findAll(attrs={"class": "review_item_header_content"})[x].text.replace(',', ' ').replace('"', '').replace('"','').replace('"', '').replace('e', 'e').strip()
            ReviewNeg = soup.findAll(attrs={"class": "review_neg"})[x].text.replace(',', ' ').replace('\n', ' ').strip()
            ReviewPost = soup.findAll(attrs={"class": "review_pos"})[x].text.replace(',', ' ').replace('\n', ' ').strip()
            RatingDate = soup.findAll(attrs={"class": "review_item_date"})[x].text.replace('Reviewed', ' ').replace('NEW',' ').replace(',', ' ').strip()
            Rating = soup.findAll(attrs={"class": "review-score-badge"})[x].text.replace(',', ' ').replace('\n', ' ').strip()

            Record = Organization + "," + Address + "," + Reviewer + "," + ReviewTitle + "," + Review + "," + RatingDate + "," + Rating
            if Checker == "REVIEWS":
                file.write(bytes(Record, encoding="ascii", errors='ignore')  + b"\n")

        link = soup.find_all(attrs={"class": "nav next taLnk "})
        print(Organization)
        if num == 15:
            break
        else:
            num = num + 5
            WebSites1 = "http://www.tripadvisor.com.ph" + "/Hotel_Review-g317121-d320846-Reviews-or" + str(num) + "-Taal_Vista_Hotel-Tagaytay_Cavite_Province_Calabarzon_Region_Luzon.html#REVIEWS"
            page = urlopen(WebSites1)
            soup = BeautifulSoup(page, "html.parser")
            print(WebSites1)
            Checker = WebSites1[-7:]

file.close()
