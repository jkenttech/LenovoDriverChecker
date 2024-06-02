from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import basic_logger as log
import sys
import re
import os

# configure selenium
options = Options()
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

def get_html(url):
    log.info(f'Downloading html data from {url}')
    try:
        browser.get(url)
        return BeautifulSoup(browser.page_source, 'html.parser')
    except:
        log.error(f'There was an error retrieving HTML data.')

def driver_query(component):
    log.info(f'Querying path {driver_query_path}{component}')
    return f'{driver_query_path}{component}'

def get_driver_versions(component):
    soup = get_html(driver_query(component))

    component = component.replace("%20", " ") # replace the %20 space with acutal space
    try:
        datarows = soup.find_all(class_="simple-table-dataRow")
        for datarow in datarows:
            title = get_title_from_datarow(component, datarow)
            datarow = datarow.find_all(class_="table-body-width-item")
            size = get_size_from_datarow(component, datarow)
            version = get_version_from_datarow(component, datarow)
            date = get_date_from_datarow(component, datarow)
            link = get_link_from_datarow(component, datarow)
            if link[0] != "/": # strips out all of the header rows as the "details" links start with /country/language/
                csv = open(f'{csv_path}', 'a')
                csv.write(f'{component};{title};{size};{version};{date};{link}\n')
            log.debug(f'{component};{title};{size};{version};{date};{link}')
    except:
        log.error(f'Unable to get all driver information for {component}')
    else:
        global componentCount
        componentCount = componentCount + 1
        log.info(f'Captured component {componentCount}/{len(components)}')

def get_title_from_datarow(component, datarow):
    try:
        return datarow.find(class_="table-body-item").find("span").text
    except:
        log.error(f'Unable to find {component} title')
        raise Exception

def get_size_from_datarow(component, datarow):
    try:
        return datarow[0].text
    except:
        log.error(f'Unable to find {component} size in {datarow}')
        raise Exception

def get_version_from_datarow(component, datarow):
    try:
        return datarow[1].text
    except:
        log.error(f'Unable to find {component} size in {datarow}')
        raise Exception

def get_date_from_datarow(component, datarow):
    try:
        return datarow[2].text
    except:
        log.error(f'Unable to find {component} date in {datarow}')
        raise Exception

def get_link_from_datarow(component, datarow):
    try:
        link = datarow[4]
        link = str(link).split("href=\"")
        link = link[1].split("\"")
        return link[0]
    except:
        log.error(f'Unable to find {component} link in {datarow}')
        log.error(f'Specific line {datarow[4]}')
        raise Exception

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

if __name__ == "__main__":
    if not os.path.exists(file_base_path):
        log.info(f'Creating driver_csv folder')
        os.makedirs(file_base_path)

    log.info(f'Downloading driver information for {serial}...')
    components = get_driver_categories()

    if len(components) < 1:
        log.error(f'Components list is empty, double check the serial number')
    else: 
        log.info(f'Number of components: {len(components)}')
        for component in components:
            get_driver_versions(component)
        if componentCount != len(components):
            log.error("There was an issue collecting all driver versions")
