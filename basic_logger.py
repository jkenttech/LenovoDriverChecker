import datetime as dt
datetime_format = "%y-%m-%d %H:%M:%S"

def info(string):
    print(f'{dt.datetime.now().strftime(datetime_format)} INF: {string}')

def error(string):
    print(f'{dt.datetime.now().strftime(datetime_format)} ERR: {string}')

def debug(string):
    print(f'{dt.datetime.now().strftime(datetime_format)} DBG: {string}')