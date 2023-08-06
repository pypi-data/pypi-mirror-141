"""Module: constants templates"""

from jinja2 import Template

DATA_PROVIDER_BASE_FILE = Template(
    '''import csv
import json
from {{ context.team_name }}.{{ context.folder_path.scripts.name }}.{{ context.folder_path.nfr_requests.name }}.{{ context.folder_path.config.name }}.CommonConfig import BASE_REQUEST_DATA_DIR


def getContent(fileName):
    """
    This method used to get content from given csv file. 
    You need to just put file in the data folder.
    :param fileName: file name as string
    :return: array of each row including header as dict format from csv file
    """
    array_content = []
    file_content = open(BASE_REQUEST_DATA_DIR+'/'+fileName, "r", encoding="utf-8")
    for line in file_content:
        array_content.append(line.strip())
    return array_content


def getContentDict(fileName):
    """
    This method used to get content from given csv file. 
    You need to just put file in the data folder.
    :param fileName: file name as string
    :return: array of each row including header as named dict format from csv file
    """
    data_file = csv.DictReader(open(BASE_REQUEST_DATA_DIR+'/'+fileName))
    data_list = []
    for row in data_file:
        data_list.append(row)
    return data_list


'''
)

