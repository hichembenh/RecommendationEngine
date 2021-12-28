from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from time import sleep
import requests

in_df = pd.read_csv('./links_to_extract.csv')

out_df = pd.DataFrame()

print('opening drive')

for i in in_df.index:
    hotel_names = []
    hotel_price = []
    hotel_ratings = []
    total_reviews = []
    hotel_url = []
    location = []
    country = []
    print((i / len(in_df))*100,'% ...')
    print('Working on', in_df['Country'][i], "hotels...")
    link = requests.get(in_df['Link_to_hotels'][i])
    if link.status_code == 200:
        driver = webdriver.chrome.webdriver.WebDriver(executable_path=r'C:/Users/21655/Desktop/chromedriver')
        driver.get(str(in_df['Link_to_hotels'][i]))
        print("Scrolling ... ")
        itheration = 0
        while itheration <= 50:
            # Scroll down to bottom
            print("Iteration", itheration + 1)
            scrolling = driver.execute_script("return document.body.scrollHeight") - 1200
            print('Scrolling', scrolling)
            driver.execute_script("window.scrollTo(0," + str(scrolling) + ")")
            # Wait to load page
            sleep(8)
            itheration += 1
        print('Getting the web page')
        web_page = driver.page_source
        soup = BeautifulSoup(web_page, 'lxml')
        # Filtering the wanted tags from the fetched html
        hotelContainer = soup.find_all("div", {"class": "-RcIiD"})
        for hotel in hotelContainer:
            hotelName = hotel.find("h2", {"class": "_3zH0kn"})
            hotelPrice = hotel.find("span", {"class": "_2R4dw5"})
            hotelRating = hotel.find("span", {"class": "_1biq31 _11XjrQ _3yXMS-"})
            totalReview = hotel.find("span", {"class": "_2jUNPN"})
            loc = hotel.find("p", {"class": "_2oHhXM"})
            hotelUrl = hotel.find("a", {"class": "_61P-R0"})
            if hotelRating is None or totalReview is None or loc is None:
                print('Passing hotel with no rating...')
                continue
            hotel_names.append(hotelName.text)
            country.append(in_df['Country'][i])
            hotel_price.append(hotelPrice.text)
            hotel_ratings.append(hotelRating.text)
            total_reviews.append(totalReview.text)
            location.append(loc.text)
            hotel_url.append(hotelUrl['href'])
        my_df = pd.DataFrame()
        my_df['country'] = country
        my_df['hotel_name'] = hotel_names
        my_df['price'] = hotel_price
        my_df['hotel_ratings'] = hotel_ratings
        my_df['total_reviews'] = total_reviews
        my_df['location'] = location
        my_df['hotel_url'] = hotel_url
        out_df = out_df.append(my_df, ignore_index=True)
        print("waiting 5 sec")
        sleep(5)
        print("Closing driver")
        driver.close()
        driver.quit()
        print(out_df)
    else:
        pass

print("Saving file...")
# Saving all the  data in a df
out_df.to_csv("links_out.csv", encoding='utf-8')
