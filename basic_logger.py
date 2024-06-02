import datetime as dt
datetime_format = "%y-%m-%d %H:%M:%S"

white = '\033[0m'
green = '\033[32m'
blue = '\033[34m'
red = '\033[31m'

def info(string):
    print(f'{dt.datetime.now().strftime(datetime_format)} {green}INF{white}: {string}')

def error(string):
    print(f'{dt.datetime.now().strftime(datetime_format)} {red}ERR{white}: {string}')

def debug(string):
    print(f'{dt.datetime.now().strftime(datetime_format)} {blue}DBG{white}: {string}')