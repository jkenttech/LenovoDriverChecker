from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import re

serial = sys.argv[1]
components = []
browser = webdriver.Chrome()
base_path = f'https://pcsupport.lenovo.com/au/en/products/{serial}'
driver_path = f'{base_path}/downloads/driver-list'
driver_query_path = f'{driver_path}/component?name='

def get_html(url):
    browser.get(url)
    return BeautifulSoup(browser.page_source, 'html.parser')


def get_driver_versions():
    for component in components:
        soup = get_html(f'{driver_query_path}{component}')
        file = open(f'driver_html/{component.replace("/","-").replace("%20", " ")}.html', 'w', encoding='utf-8')
        file.write(str(soup.prettify))
        for datarow in soup.find_all(class_="simple-table-dataRow"):
            title = datarow.find(class_="table-body-item").find("span").text
            version = datarow.find_all(class_="table-body-width-item")
            csv = open(f'drivers.csv', 'a')
            csv.write(f'{title};{version[0].text};{version[1].text};{version[2].text}\n')

def get_driver_categories():
    soup = get_html(f'{driver_path}')
    raw_categories = soup.find_all(class_="title-row")
    category_list = []
    for category in raw_categories:
        category = re.sub(r'\s\(\d{0,}\)\s?$', '', category.text)
        category = re.sub(r'\s', '%20', category)
        category_list.append(category)
    return category_list

if __name__ == "__main__":
    print("running on main")
    print(f'serial number is {serial}')
    components = get_driver_categories()
    get_driver_versions()
