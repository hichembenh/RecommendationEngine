from bs4 import BeautifulSoup
from selenium import webdriver


SCRAP_URL = "https://www.expedia.fr/Tunis-Hotel-Hotel-Africa.h1200137.Description-Hotel?chkin=2022-01-09&chkout=2022-01-10&x_pwa=1&rfrr=HSR&pwa_ts=1640549046057&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5mci9Ib3RlbC1TZWFyY2g%3D&useRewards=false&rm1=a2&regionId=3570&destination=Tunis%2C+Gouvernorat+de+Tunis%2C+Tunisie&destType=MARKET&neighborhoodId=553248622847082628&sort=RECOMMENDED&top_dp=60&top_cur=EUR&semdtl=&userIntent=&selectedRoomType=123076&selectedRatePlan=202069895"

driver = webdriver.chrome.webdriver.WebDriver(executable_path=r'C:/Users/21655/Desktop/chromedriver')

soup = BeautifulSoup(SCRAP_URL)

