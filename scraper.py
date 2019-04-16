from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

import xlsxwriter

# Create an new Excel file and add a worksheet
workbook = xlsxwriter.Workbook('connolly.xlsx')
worksheet = workbook.add_worksheet()

chromedriver_path = '/usr/local/bin/chromedriver' # TO AMEND
driver = webdriver.Chrome(executable_path=chromedriver_path)

url = 'https://factfinder.census.gov/faces/nav/jsf/pages/searchresults.xhtml?refresh=t'
driver.get(url)

topics = driver.find_element_by_xpath('//*[@id="topic-overlay-btn"]')
driver.execute_script("arguments[0].click()", topics)

driver.implicitly_wait(50)

people = driver.find_element_by_xpath('//*[@id="ygtvt88"]/a')
people.click()

income_earnings = driver.find_element_by_xpath('//*[@id="ygtvt101"]/a')
income_earnings.click()

household_ie = driver.find_element_by_xpath('//*[@id="ygtvlabelel189"]/span')
household_ie.click()

geographies = driver.find_element_by_xpath('//*[@id="geo-overlay-btn"]')
driver.execute_script("arguments[0].click()", geographies)

driver.implicitly_wait(50)

geo_type = Select(driver.find_element_by_xpath('//*[@id="summaryLevel"]'))
geo_type.select_by_value("150")

geo_values = driver.find_elements_by_xpath('//*[@id="state"]/option')
geos = [val.get_attribute("value").encode("ascii", "ignore") for val in geo_values]
print geos

select_state = Select(driver.find_element_by_xpath('//*[@id="state"]'))

for i in range(1, len(geos)):

    select_state.select_by_value(geos[i])

    driver.implicitly_wait(50)

    county_values = driver.find_elements_by_xpath('//*[@id="county"]/option')
    counties = [val.get_attribute("value").encode("ascii", "ignore") for val in county_values]
    print counties

    select_county = Select(driver.find_element_by_xpath('//*[@id="county"]'))

    for j in range(1, len(counties)):
        time.sleep(2)

        select_county = Select(driver.find_element_by_xpath('//*[@id="county"]'))
        select_county.select_by_value(counties[j])

        driver.implicitly_wait(50)

        select_geo_list = Select(driver.find_element_by_xpath('//*[@id="geoAssistList"]'))
        select_geo_list.select_by_index(0)
        # select_geo_list = driver.find_element_by_xpath('//*[@id="geoAssistList"]/option')
        # driver.execute_script("arguments[0].click()", select_geo_list)

        driver.implicitly_wait(50)

        # add to selections
        add_to_selections = driver.find_element_by_xpath('//*[@id="geocommon"]/span/a[1]')
        driver.execute_script("arguments[0].click()", add_to_selections)

        time.sleep(2)

close = driver.find_element_by_xpath('//*[@id="geo-overlay"]/div[2]/a[3]/img')
driver.execute_script("arguments[0].click()", close)
household_income_12mo = driver.find_element_by_xpath("//a[contains(text(), 'HOUSEHOLD INCOME IN THE PAST 12 MONTHS')]")
driver.execute_script("arguments[0].click()", household_income_12mo)

time.sleep(2)

download = driver.find_element_by_xpath('//*[@id="dnld_btn"]')
# driver.execute_script("arguments[0].click()", download)
download.click()

time.sleep(2)

use_data = driver.find_element_by_xpath('//*[@id="dnld_decision_use"]')
use_data.click()

ok_btn = driver.find_element_by_xpath("//button[contains(text(), 'OK')]")
ok_btn.click()
time.sleep(2)

download_finally = driver.find_element_by_xpath("//button[contains(text(), 'Download')]")
download_finally.click()
