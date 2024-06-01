import datetime as dt

def info(string):
    print(f'{dt.datetime.now()} INF: {string}')

def error(string):
    print(f'{dt.datetime.now()} ERR: {string}')

def debug(string):
    print(f'{dt.datetime.now()} DBG: {string}')