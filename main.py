# pip imports
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# standard library imports
import sys
import re
# local imports
import basic_logger as log # singleton
from csv_writer import csv_writer # import class
import datarow as row # singleton
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

def get_html(url): # download the html data
    try:
        browser.get(url)
        return BeautifulSoup(browser.page_source, 'html.parser')
    except:
        log.error(f'There was an error retrieving HTML data.')
# end get_html(url)

def query_driver(component):
    log.info(f'Querying path {driver_query_path}{component}')
    return f'{driver_query_path}{component}'
# end driver_query(component)

def get_driver_versions(component):
    driver_versions = []
    soup = get_html(query_driver(component))

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

def main():
    writer = csv_writer(serial)

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
        writer.write_to_csv(driver_list)
        if componentCount != len(components):
            log.error("There was an issue collecting all driver versions")
# end main()

if __name__ == "__main__":
    main()
# end if __name__ == "__main__":
