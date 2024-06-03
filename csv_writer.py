import basic_logger as log
import os

class csv_writer:
    file_base_path = f'driver_csv'

    def __init__(self, serial):
        self.serial = serial
        self.csv_path = f'{self.file_base_path}/{self.serial}_drivers.csv'
        self.check_path_exists()
    # end __init__(self, serial):


    def write_to_csv(self, driver_list):
        csv = open(f'{self.csv_path}', 'a')
        for driver in driver_list:
            csv.write(f'{driver}\n')
        csv.close()
    # writeToCSV(driver_list)

    def check_path_exists(self):
        if not os.path.exists(self.file_base_path):
            log.info(f'Creating driver_csv folder')
            os.makedirs(self.file_base_path)