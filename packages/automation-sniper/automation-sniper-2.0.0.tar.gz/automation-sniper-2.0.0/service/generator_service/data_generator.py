import re
import logging
import os
import shutil
import csv
from service.utils.logger import get_logger

logger = get_logger()


class DataGenerator:
    def __init__(self, data_path):
        logger = get_logger(os.environ)
        self.data_folder = data_path

    def generate_and_write_csv_file(self, file_name: str, header_data: dict):
        header = []
        if os.path.isfile(self.data_folder + "/" + file_name+".csv"):
            csv_data = csv.reader(open(self.data_folder + "/" + file_name+".csv", 'r', encoding='UTF8'))
            for row in csv_data:
                header = header+row
        for key, value in header_data.items():
            header.append(key+"/"+str(value))
        header = list(set(header))
        with open(self.data_folder + "/" + file_name+".csv", 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        return file_name+".csv"

