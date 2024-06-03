# standard library imports
import sys
# local imports
import basic_logger as log # singleton
from csv_writer import csv_writer 
from driver_handler import driver_handler
# end of imports

# local variables
serial = sys.argv[1]
components = []
componentCount = 0

def main():
    writer = csv_writer(serial)
    handler = driver_handler(serial)

    log.info(f'Downloading driver information for {serial}...')
    global components
    components = handler.get_driver_categories()

    if len(components) < 1:
        log.error(f'Components list is empty, double check the serial number')
    else: 
        log.info(f'Number of components: {len(components)}')
        driver_list = []
        for component in components:
            driver_list.extend(handler.get_driver_versions(component))
        # end for
        writer.write_to_csv(driver_list)
        if componentCount != len(components):
            log.error("There was an issue collecting all driver versions")
        # end if
    # end else
# end main()

if __name__ == "__main__":
    main()
# end if __name__ == "__main__":
