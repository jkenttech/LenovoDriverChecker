# Lenovo Driver Checker
Scans the Lenovo PCSupport site for current driver versions and adds the drivers to a csv file
NOTE: the csv that is output is deliniated by semicolons, not commas, as driver titles occasionally use commas. When importing the csv make sure to use the semicolon delimiter
## Installation
1. Setup the venv:
  - python -m venv .venv
2. Install BeautifulSoup and Selenium
  - python -m pip install beautifulsoup4
  - python -m pip install selenium
3. Download the ChromeDriver for selenium and put it in the root folder (app was created with version 125.0.6422.141)
  - https://googlechromelabs.github.io/chrome-for-testing/

## Running the app
The typical command is "$PYTHON $MAIN $SERIALNUMBER", e.g. "python main.py serialnumber", ".venv/bin/python main.py serialnumber"
Examples:
  - python main.py MP32MXX
  - python main.py PF44AHKA
App also works with MTs.
  - python main.py 20S0
  - python main.py 20XX

