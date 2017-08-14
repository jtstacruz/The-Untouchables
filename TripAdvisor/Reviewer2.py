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
    "https://www.agoda.com/taal-vista-hotel/hotel/tagaytay-ph.html#REVIEWS"]
Checker = "REVIEWS"
# looping through each site until it hits a break
num = 5
for theurl in WebSites:
    thepage = urlopen(theurl)
    soup = BeautifulSoup(thepage, "html.parser")
    while True:
        # extract the help count, restaurant review count, attraction review count and hotel review count
        a = b = 0
        helpcountarray = restaurantarray = attractionarray = hotelarray = ""
        WebSites1 = ""

        for profile in soup.findAll(attrs={"class": "col-xs-3 review-info"}):
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

            if image.find("attraction") > 0:
                counter = image.split("attraction", 1)[0].split("|", 1)[1][-4:].replace("|", "").strip()
                if len(attractionarray) == 0:
                    attractionarray = [counter]
                else:
                    attractionarray.append(counter)
            elif image.find("attraction") < 0:
                if len(attractionarray) == 0:
                    attractionarray = ["0"]
                else:
                    attractionarray.append("0")

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

                # extract the rating count for each user review
        altarray = ""   
        for rating in soup.findAll(attrs={"class": "rating reviewItemInline"}):
            #alt = rating.find('img', alt=True)['alt']
            #if alt[-5:] == 'stars':
            #    if len(altarray) == 0:
            #        altarray = [alt]
            #    else:
            #        altarray.append(alt)

            #if rating.find(class_ = "ui_bubble_rating bubble_50"):     
            #    print(50)
            #elif rating.find(class_ = "ui_bubble_rating bubble_40"):    
            #    print(40)
            
            alt = rating.find('span', class_='ui_bubble_rating', alt=True)['alt']
            if alt is not None:
                if alt[-5:] == 'bubbles':
                    if len(altarray) == 0:
                       altarray = [alt]
                    else:
                      altarray.append(alt)
            elif alt is None:
                    print("No rating!")


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
            RatingDate = soup.findAll(attrs={"class": "reviewdate"})[x].text.replace('Reviewed', ' ').replace('NEW',' ').replace(',', ' ').strip()
            Rating = altarray[x]

            Record = Organization + "," + Address + "," + Reviewer + "," + ReviewTitle + "," + Review + "," + RatingDate + "," + Rating
            if Checker == "REVIEWS":
                file.write(bytes(Record, encoding="ascii", errors='ignore')  + b"\n")

        link = soup.find_all(attrs={"class": "nav next taLnk "})
        print(Organization)
        if num == 10:
            break
        else:
            num = num + 5
            WebSites1 = "http://www.tripadvisor.com.ph" + "/Hotel_Review-g317121-d320846-Reviews-or" + str(num) + "-Taal_Vista_Hotel-Tagaytay_Cavite_Province_Calabarzon_Region_Luzon.html#REVIEWS"
            page = urlopen(WebSites1)
            soup = BeautifulSoup(page, "html.parser")
            print(WebSites1)
            Checker = WebSites1[-7:]

file.close()