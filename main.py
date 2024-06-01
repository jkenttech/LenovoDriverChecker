from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import sys

serial = "MP09RFK7"
components = [ 'Audio', 'BIOS/UEFI']

browser = webdriver.Chrome()

for component in components:
    url = f'https://pcsupport.lenovo.com/au/en/products/{serial}/downloads/driver-list/component?name={component}'
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    file = open(f'{component.replace("/","")}.html', 'w', encoding='utf-8')
    file.write(str(soup.prettify))
    for datarow in soup.find_all(class_="simple-table-dataRow"):
        title = datarow.find(class_="table-body-item").find("span").text
        version = datarow.find_all(class_="table-body-width-item")
        print(f'{title}\t{version[0].text}\t{version[1].text}\t{version[2].text}')
