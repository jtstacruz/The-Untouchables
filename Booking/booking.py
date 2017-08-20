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
    b"Organization,Reviewer,Address,Review Title,,Review,Rating Date,Rating" + b"\n")

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
        helpcountarray = hotelarray = ""
        WebSites1 = ""

        for profile in soup.findAll(attrs={"class": "review_item_review"}):
            image = profile.text.replace("\n", "|||||").strip()
            if image.find("helpful vote") > 0:
                counter = image.split("helpful vote", 1)[0].split("|", 1)[1][-4:].replace("|", "").strip()
                if len(helpcountarray) == 0:
                    helpcountarray = [counter]
                else:
                    helpcountarray.append(counter)
            elif image.find("helpful vote") < 0:
                if len(helpcountarray) == 0:
                    helpcountarray = ["0"]
                else:
                    helpcountarray.append("0")

        Organization = "Taal Vista Hotel"

                # Loop through each review on the page
        for x in range(0, len(helpcountarray)):
            try:
                User = soup.findAll("h4")[x].text
                Reviewer = User[0]
            except:
                Reviewer = "N/A"
                continue

            Reviewer = Reviewer.replace(',', ' ').replace('"', '').replace('"', '').replace('"', '').strip()
            Address = soup.findAll(attrs={"class": "reviewer_country"})[x].text.replace(',', ' ').replace('\n', ' ').strip()
            ReviewTitle = soup.findAll(attrs={"class": "review_item_header_content"})[x].text.replace(',', ' ').replace('"', '').replace('"','').replace('"', '').replace('e', 'e').strip()
            RatingDate = soup.findAll(attrs={"class": "review_item_date"})[x].text.replace('Reviewed', ' ').replace('NEW',' ').replace(',', ' ').strip()
            Rating = soup.findAll(attrs={"class": "review-score-badge"})[x].text.replace(',', ' ').replace('\n', ' ').strip()
            Review = soup.findAll(attrs={"class": "review_neg"})[x].text.replace(',', ' ').replace('\n', ' ').strip()

            Record = Organization + "," + Reviewer + "," + Address +  "," + ReviewTitle + "," + Review + "," + RatingDate + "," + Rating
            if Checker == "REVIEWS":
                file.write(bytes(Record, encoding="ascii", errors='ignore')  + b"\n")

            Review = soup.findAll(attrs={"class": "review_pos"})[x].text.replace(',', ' ').replace('\n', ' ').strip()

            Record = Organization + "," + Reviewer + "," + Address +  "," + ReviewTitle + "," + Review + "," + RatingDate + "," + Rating
            if Checker == "REVIEWS":
                file.write(bytes(Record, encoding="ascii", errors='ignore')  + b"\n")

        link = soup.find('p', attrs={"class": "page_link review_next_page"})
        print(Organization)
        print(link)
        if link.findAll('href'):
            soup = BeautifulSoup(urllib.request.urlopen("https://www.booking.com" + link[0].get('href')),"html.parser")
            print(link[0].get('href'))
            Checker = link[0].get('href')[-7:]
        else:
            break


file.close()
