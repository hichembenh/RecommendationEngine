from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException, \
    NoSuchWindowException, TimeoutException
import csv
import requests
from selenium.webdriver.common.by import By

SCARP_URL = "https://www.expedia.fr/"
out_df = pd.DataFrame()

country_list_file = open('country_list.csv', 'r')
csv_reader = csv.reader(country_list_file)
countries = []
for row in csv_reader:
    countries.append(row)
country_list_file.close()

for i, item in enumerate(countries):
    driver = webdriver.chrome.webdriver.WebDriver(executable_path=r'C:/Users/21655/Desktop/chromedriver')
    print("opening driver")
    hetels_incountry_link = SCARP_URL + "Hotel-Search?destination=" + item[0]
    # Handeling redirection
    print("Lookin for Hotels in %s .. " % (item[0]))
    search_list_to_prase_link = requests.get(str(hetels_incountry_link))
    # Fetching all available hotels with show more button
    driver.get(search_list_to_prase_link.url)
    print("Prasinng ... ")
    sleep(20)
    try:
        while driver.find_element(By.XPATH, '//*[@data-stid="show-more-results"]'):
            driver.find_element(By.XPATH, '//*[@data-stid="show-more-results"]').click()
    except (NoSuchElementException, StaleElementReferenceException, WebDriverException, NoSuchWindowException,TimeoutException):
        print("No more Hotels")
        print("Counting Hotels... ")

    # Fetch the html
    web_page = driver.page_source
    soup = BeautifulSoup(web_page)
    # Filtering the wanted tags from the fetched html
    all_hotel_tags = soup.find_all("li",
                                   {"class": "uitk-spacing listing uitk-spacing-margin-blockstart-three horizontal"})
    print("found %d hotels in %s" % (len(all_hotel_tags), item[0]))
    print("putting them in a csv file ")
    # getting the desired link
    for hotel_tag in all_hotel_tags:
        stair = hotel_tag.find_all("a")
        # stair = hotel_tag.find_element(By.XPATH, '//*[@dara-stid="open-hotel-information"]')
        hotel_link = stair[1].attrs['href']
        print(hotel_link)
        dict_to_add = {"Country": item[0],
                       "link_to_hotel": str(hotel_link)}
        print(dict_to_add)
        out_df = out_df.append(dict_to_add, ignore_index=True)
    # Quittting the selenium driver
    print("waiting 5 sec")
    sleep(5)
    print("Closing driver")
    driver.close()
    driver.quit()
    print(out_df)

# Saving all the  data in a df
out_df.to_csv("links_out.csv", encoding='utf-8')
