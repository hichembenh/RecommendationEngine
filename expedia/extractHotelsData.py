from time import sleep
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

SCRAP_URL = "https://www.expedia.fr/Djerba-Midun-Hotel-Seabel-Rym-Beach-Djerba.h1378658.Description-Hotel?chkin=2022-01-10&chkout=2022-01-11&x_pwa=1&rfrr=HSR&pwa_ts=1640579425337&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5mci9Ib3RlbC1TZWFyY2g%3D&useRewards=false&rm1=a2&regionId=182&destination=Tunisie&destType=MARKET&sort=RECOMMENDED&top_dp=82&top_cur=EUR&semdtl=&userIntent=&selectedRoomType=419535&selectedRatePlan=1450373"

driver = webdriver.chrome.webdriver.WebDriver(executable_path=r'C:/Users/21655/Desktop/chromedriver')

try:
    url = requests.get(SCRAP_URL)
    print("URL is valid and exists on the internet")
    driver.get(str(url.url))
    print("Prasinng ... ")
    sleep(50)
    print('opening driver')
    web_page = driver.page_source
    soup = BeautifulSoup(web_page, 'lxml')

    # Getting hotel name
    hotelName = soup.title.text

    # Getting location
    location = soup.find('div', {
        'class': 'uitk-text uitk-type-300 uitk-flex-item uitk-flex-basis-full_width uitk-text-default-theme'
    }).text

    # Getting stars
    starsDiv = soup.find('div', {'class': 'uitk-rating'})
    stars = starsDiv.find('span', {'class': 'is-visually-hidden'})

    # Getting rating
    ratingTag = soup.find('meta', {'itemprop': 'ratingValue'})

    # Getting number of reviews
    reviewCount = soup.find('meta', {'itemprop': 'reviewCount'})
    roomTag = soup.find('section', {'class': 'main-region infosite__main'})
    priceTage = roomTag.find('div', {"data_stid": "price-lockup-wrapper"})
    print(soup.prettify())
    nomberExperience = reviewCount['content']
    rating = ratingTag['content']
    driver.close()
    driver.quit()
    print(priceTage)
    print(hotelName, 'in:', location, 'rating:', rating, "review count: ", nomberExperience)
except requests.ConnectionError as exception:
    print("URL does not exist on Internet")
