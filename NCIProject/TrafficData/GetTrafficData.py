import datetime
from selenium import webdriver
from TrafficData import GetDownloadLinks

driver = webdriver.Chrome("C:/Users/myusuf/accela/AccelaTestAutomation/"
                          "AccelaUITests/src/test/resources/drivers/Chromedriver.exe")

fromDate = datetime.date(2019,11,15)
toDate = datetime.datetime.now().date() - datetime.timedelta(1)

urls = GetDownloadLinks.geturls(fromDate, toDate)

# download the files in download directory
for url in urls:
    driver.get(url)

