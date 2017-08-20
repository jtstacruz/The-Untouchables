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
        hotelarray = ""
        WebSites1 = ""

        for profile in soup.findAll(attrs={"class": "col-xs-3 review-info"}):
            if span.find("Stayed") > 0:
                counter = span.split("Stayed", 1)[0].split("|", 1)[1][-4:].replace("|", "").strip()
                if len(hotelarray) == 0:
                    hotelarray = [counter]
                else:
                    hotelarray.append(counter)
            elif span.find("Stayed") < 0:
                if len(hotelarray) == 0:
                    hotelarray = ["0"]
                else:
                    hotelarray.append("0")

        Organization = "Taal Vista"
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

        link = soup.find_all(attrs={"class": "next-arrow"})
        print(Organization)
        print(link)
        if len(link) == 0:
            break
        else:
            soup = BeautifulSoup(urllib.request.urlopen("http://www.tripadvisor.com" + link[0].get('href')),"html.parser")
            print(link[0].get('href'))
            Checker = link[0].get('href')[-7:]

file.close()
