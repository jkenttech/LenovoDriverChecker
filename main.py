from bs4 import BeautifulSoup
import requests
import sys

serial = "MP09RFK7"
components = [ 'Audio' , 'BIOS/UEFI']

for component in components:
    url = f'https://pcsupport.lenovo.com/au/en/products/{serial}/downloads/driver-list/component?name={component}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    file = open(f'{component}.html', 'w', encoding='utf-8')
    file.write(str(soup.prettify))
