# pip imports
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# standard library imports
import re
# import local modules
import basic_logger as log # singleton
import datarow as row # singleton

class driver_handler:
    # configure selenium
    options = Options()
    # options.add_argument('--headless=old')
    options.add_argument('-no-sandbox')
    options.add_argument('incognito')
    browser = webdriver.Chrome(options)

    # variables required throughout the class
    components = []

    def __init__(self, serial):
        self.url_base_path = f'https://pcsupport.lenovo.com/au/en/products/{serial}'
        self.driver_path = f'{self.url_base_path}/downloads/driver-list'
        self.driver_query_path = f'{self.driver_path}/component?name='
        self.componentCount = 0
    # end __init__(self, serial):

    def get_html(self, url): # download the html data
        try:
            self.browser.get(url)
            return BeautifulSoup(self.browser.page_source, 'html.parser')
        except:
            log.error(f'There was an error retrieving HTML data.')
    # end get_html(url)

    def query_driver(self, component):
        log.info(f'Querying path {self.driver_query_path}{component}')
        return f'{self.driver_query_path}{component}'
    # end driver_query(component)

    def get_driver_versions(self, component):
        driver_versions = []
        soup = self.get_html(self.query_driver(component))

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
                # end if
            # end for
        except:
            log.error(f'Unable to get all driver information for {component}')
        else:
            self.componentCount += 1
            log.info(f'Captured component {self.componentCount}/{len(self.components)}')
            return driver_versions
        # end else
    # end get_driver_versions(component)

    def get_driver_categories(self):
        log.info(f'Getting driver categories...')
        soup = self.get_html(f'{self.driver_path}')
        raw_categories = soup.find_all(class_="title-row")
        category_list = []
        for category in raw_categories:
            category = re.sub(r'\s\(\d{0,}\)\s?$', '', category.text)
            category = re.sub(r'\s', '%20', category)
            category_list.append(category)
        self.components = category_list
        return category_list
    # get_driver_categories()