# tripadvisor Scrapper - use this one to scrape hotels

# importing libraries
from bs4 import BeautifulSoup
import urllib
import os
import re
from urllib.request import urlopen

# creating CSV file to be used

file = open(os.path.expanduser(r"~/Desktop/Agoda Reviews.csv"), "wb")
file.write(
    b"Organization,Address,Reviewer,Review Title,Review,Rating Date,Rating" + b"\n")

# List the first page of the reviews (ends with "#REVIEWS") - separate the websites with ,
WebSites = [
    "https://www.agoda.com/taal-vista-hotel/hotel/tagaytay-ph.html"]
Checker = "REVIEWS"
# looping through each site until it hits a break
num = 0
for theurl in WebSites:
    thepage = urlopen(theurl)
    soup = BeautifulSoup(thepage, "html.parser")
    while True:
        # extract the help count, restaurant review count, attraction review count and hotel review count
        a = b = 0
        helpcountarray = ""
        WebSites1 = ""

        for profile in soup.findAll(attrs={"class": "member_info"}):
            if span.find("Did you find this review helpful?") > 0:
                counter = span.split("Did you find this review helpful?", 1)[0].split("|", 1)[1][-4:].replace("|", "").strip()
                if len(helpcountarray) == 0:
                    helpcountarray = [counter]
                else:
                    helpcountarray.append(counter)
            elif span.find("Did you find this review helpful?") < 0:
                if len(helpcountarray) == 0:
                    helpcountarray = ["0"]
                else:
                    helpcountarray.append("0")

        Organization = soup.find(attrs={"class": "hotel-header-name"}).text.replace('"', ' ').strip()
        Address = "Tagaytay City"

        # Loop through each review on the page
        for x in range(0, len(hotelarray)):
            try:
                Reviewer = soup.findAll(attrs={"class": "reviewer-name"})[x].text
            except:
                Reviewer = "N/A"
                continue

            Reviewer = Reviewer.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').strip()
            ReviewTitle = soup.findAll(attrs={"class": "comment-title-text"})[x].text.replace(',', ' ').replace('"', '').replace('"','').replace('"', '').replace('e', 'e').strip()
            Review = soup.findAll(attrs={"class": "comment-text"})[x].text.replace(',', ' ').replace('\n', ' ').strip()
            RatingDate = soup.findAll(attrs={"class": "comment-text"})[x].text.replace('Reviewed', ' ').replace('NEW',' ').replace(',', ' ').strip()
            Rating = soup.findAll(attrs={"class": "individual-review-rate"})[x].text.replace(',', ' ').replace('\n', ' ').strip()

            Record = Organization + "," + Address + "," + Reviewer + "," + ReviewTitle + "," + Review + "," + RatingDate + "," + Rating
            if Checker == "REVIEWS":
                file.write(bytes(Record, encoding="ascii", errors='ignore')  + b"\n")

        link = soup.find_all(attrs={"class": "nav next taLnk "})
        print(Organization)
        print(link)
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
