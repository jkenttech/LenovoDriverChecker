import basic_logger as log

def get_title_from_datarow(component, datarow):
    try:
        return datarow.find(class_="table-body-item").find("span").text
    except:
        log.error(f'Unable to find {component} title')
        raise Exception
# end get_title_from_datarow(component, datarow)

def get_size_from_datarow(component, datarow):
    try:
        return datarow[0].text
    except:
        log.error(f'Unable to find {component} size in {datarow}')
        raise Exception
# end get_size_from_datarow(component, datarow)

def get_version_from_datarow(component, datarow):
    try:
        return datarow[1].text
    except:
        log.error(f'Unable to find {component} size in {datarow}')
        raise Exception
# end get_version_from_datarow(component, datarow)

def get_date_from_datarow(component, datarow):
    try:
        return datarow[2].text
    except:
        log.error(f'Unable to find {component} date in {datarow}')
        raise Exception
# end get_date_from_datarow(component, datarow)

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
# end get_link_from_datarow(component, datarow)
