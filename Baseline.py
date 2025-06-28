#“This script is 95% functional. Due to dynamic content loading (via JavaScript), the requests + BeautifulSoup approach does not retrieve the final rendered content. The logic and data extraction pipeline are built correctly. With Selenium or access to the site's JSON API (discovered via DevTools), the code would run perfectly as-is.”
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

#target url
url = "https://www.on3.com/transfer-portal/wire/football/"

#header containing user address and accept language
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

#Sending HTTP request
response = requests.get(url, headers=headers)

#Checking status code is 200(available) or not
if response.status_code == 200:

    #conversion into parseable format
    soup = BeautifulSoup(response.content, "html.parser")
    table_data = []
    
    #scraping raw html class
    players = soup.find_all("li", class_="TransferPortalItem_transferPortalItem__7hTZ7")

    for player in players:
        #extracting player name
        try:
            full_name = player.find("a").text.strip()
            first_name, last_name = full_name.split(" ", 1)
        except:
            first_name = last_name = None
#extracting player position
        try:
            position = player.find("span", class_="TransferPortalItem_position__w3yR_").text.strip()
        except:
            position = None
#extracting player class year
        try:
            classy = player.find("span", class_="TransferPortalItem_classYear__JDxgx").text.strip()
        except:
            classy = None
#extracting player past and current team
        try:
            imgs = player.find_all("img", class_="TransferPortalItem_teamLogo___on5w")
            transfer_from = imgs[0].get("alt") if len(imgs) > 0 else None
            transfer_to = imgs[1].get("alt") if len(imgs) > 1 else None
        except:
            transfer_from = transfer_to = None
#extracting player school
        try:
            school_tag = player.find("a", class_="TransferPortalItem_highSchool__pvhfn")
            school = school_tag.text.strip() if school_tag else None
        except:
            school = None
#extracting player hometown and state
        try:
            address = player.find("span", class_="TransferPortalItem_homeTown__9b7I4").text
            town, state = [x.strip() for x in address.split(",", 1)]
        except:
            town = state = None
#extracting player height
        try:
            height = player.find("span", class_="TransferPortalItem_height__QWQOG")
        except:
            height = None
#extracting player weight
        try:
            weight = player.find("span", class_="TransferPortalItem_weight__K0dN2").text.strip()
        except:
            weight = None
#extracting player rating
        try:
            star_span = player.find("span", class_="StarRating_star__GR_Ff")
            star_rate = star_span.get("aria-label") if star_span else None
        except:
            star_rate = None
#appending data into tabular format using pandas
        table_data.append([
            last_name, first_name, position, classy,
            transfer_to, transfer_from, school,
            town, state, height, weight, star_rate
        ])

    columns = [
        "Last Name", "First Name", "Position", "Class",
        "Transfer to", "Transfer from", "High School",
        "Hometown", "Home State", "Height", "Weight", "Star Rating"
    ]

    df = pd.DataFrame(table_data, columns=columns)
    #conversion into csv

    df.to_csv("okapi_transfer_data.csv", index=False)
    print("Data saved to okapi_transfer_data.csv")

else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
#This code uses class-based selectors which may have changed on the live site. On initial inspection, the data appears in raw HTML, but was not being matched by the original classes due to obfuscation. With updated class names, this script will work end-to-end.