from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import basic_logger as log
import sys
import re
import os

# configure selenium
try:
    if(sys.argv[2] == 'firefox'):
        options = webdriver.FirefoxOptions()
        browser = webdriver.Firefox(options)
except:
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--incognito')
    browser = webdriver.Chrome(options)

# local variables
serial = sys.argv[1]
components = []

# paths
url_base_path = f'https://pcsupport.lenovo.com/au/en/products/{serial}'
driver_path = f'{url_base_path}/downloads/driver-list'
driver_query_path = f'{driver_path}/component?name='
file_base_path = f'{serial}_driver_html/'
csv_path = f'{serial}_drivers.csv'

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
    file_path = f'{file_base_path}{component.replace("/","-").replace("%20", " ")}.html'

    try:
        file = open(file_path, 'w', encoding='utf-8')
        file.write(str(soup.prettify))
        for datarow in soup.find_all(class_="simple-table-dataRow"):
            title = datarow.find(class_="table-body-item").find("span").text
            version = datarow.find_all(class_="table-body-width-item")
            csv = open(f'{csv_path}', 'a')
            csv.write(f'{title};{version[0].text};{version[1].text};{version[2].text}\n')
    except:
        log.error(f'Unable to write to {file_path}')

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
        log.info(f'Creating driver_html folder')
        os.makedirs(file_base_path)

    log.info(f'Downloading driver information for {serial}...')
    components = get_driver_categories()

    if len(components) < 1:
        log.error(f'Components list is empty, double check the serial number')
    else: 
        for component in components:
            get_driver_versions(component)
