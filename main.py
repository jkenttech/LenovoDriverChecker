# pip imports
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# standard library imports
import sys
import re
import os
# local imports
import basic_logger as log
import datarow as row
# end of imports

# configure selenium
options = Options()
# options.add_argument('--headless=old')
options.add_argument('-no-sandbox')
options.add_argument('incognito')
browser = webdriver.Chrome(options)

# local variables
serial = sys.argv[1]
components = []
componentCount = 0

# paths
url_base_path = f'https://pcsupport.lenovo.com/au/en/products/{serial}'
driver_path = f'{url_base_path}/downloads/driver-list'
driver_query_path = f'{driver_path}/component?name='
file_base_path = f'driver_csv'
csv_path = f'{file_base_path}/{serial}_drivers.csv'

def get_html(url): # download the html data
    try:
        browser.get(url)
        return BeautifulSoup(browser.page_source, 'html.parser')
    except:
        log.error(f'There was an error retrieving HTML data.')
# end get_html(url)

def driver_query(component):
    log.info(f'Querying path {driver_query_path}{component}')
    return f'{driver_query_path}{component}'
# end driver_query(component)

def get_driver_versions(component):
    driver_versions = []
    soup = get_html(driver_query(component))

    component = component.replace("%20", " ") # replace the %20 space with acutal space
    component = component.replace(",", "") # replace comma with space for clean csv output
    try:
        datarows = soup.find_all(class_="simple-table-dataRow")
        for datarow in datarows:
            title = row.get_title_from_datarow(component, datarow).replace(",","")
            datarow = datarow.find_all(class_="table-body-width-item")
            size = row.get_size_from_datarow(component, datarow).replace(",","")
            version = row.get_version_from_datarow(component, datarow).replace(",","")
            date = row.get_date_from_datarow(component, datarow).replace(",","")
            link = row.get_link_from_datarow(component, datarow)
            if link[0] != "/": # strips out all of the header rows as the "details" links start with /country/language/
                current_driver = f'{component},{title},{size},{version},{date},{link}'
                driver_versions.append(current_driver)
    except:
        log.error(f'Unable to get all driver information for {component}')
    else:
        global componentCount
        componentCount = componentCount + 1
        log.info(f'Captured component {componentCount}/{len(components)}')
        return driver_versions
# end get_driver_versions(component)

def get_driver_categories():
    log.info(f'Getting driver categories...')
    soup = get_html(f'{driver_path}')
    raw_categories = soup.find_all(class_="title-row")
    category_list = []
    for category in raw_categories:
        category = re.sub(r'\s\(\d{0,}\)\s?$', '', category.text)
        category = re.sub(r'\s', '%20', category)
        category_list.append(category)
    return category_list
# get_driver_categories()

def writeToCSV(driver_list):
        csv = open(f'{csv_path}', 'a')
        for driver in driver_list:
            csv.write(f'{driver}\n')
        csv.close()
# writeToCSV(driver_list)

def main():
    if not os.path.exists(file_base_path):
        log.info(f'Creating driver_csv folder')
        os.makedirs(file_base_path)

    log.info(f'Downloading driver information for {serial}...')
    global components
    components = get_driver_categories()

    if len(components) < 1:
        log.error(f'Components list is empty, double check the serial number')
    else: 
        log.info(f'Number of components: {len(components)}')
        driver_list = []
        for component in components:
            driver_list.extend(get_driver_versions(component))
        writeToCSV(driver_list)
        if componentCount != len(components):
            log.error("There was an issue collecting all driver versions")
# end main()

if __name__ == "__main__":
    main()
# end if __name__ == "__main__":
