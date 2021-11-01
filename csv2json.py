#!/usr/bin/python3.9
"""
//! objectives:
//! Download any csv from web (cols > 5, rows > 10)
//! Cache option, if True use cached version instead of downloading
//! Settings in yaml response (use_cache, cache_folder, output_format, etc)
//! Logger that logs every step
! Read the response's first 5 cols and 10 rows
//! Output the result to json or csv depending on settings (make both options)
"""

import csv
import json
import logging
import requests
import yaml
import sys
import os
from collections import OrderedDict

# logging configuration section
logging.basicConfig(filename='runtime.log',
                    encoding='utf-8',
                    level=logging.DEBUG)
logging.debug('up and running')
logging.debug('read configs.yaml')

# think that more clear solution for chaching purposes, is
# to store cached data in ordered dict. This type of dictionary
# save their data in order this data been added
logging.debug('cache defned localy in OrderedDict')
cache = OrderedDict()


# reading config file
logging.debug('read configuration file')
with open('configs.yaml', 'r') as f:
    logging.debug('loading configurations')
    config = yaml.load(f, Loader=yaml.FullLoader)
    f.close()  # access internal config's data with config[str(dataname)]


def is_file_local(object):
    directory = [file for file in os.listdir('.')]
    return object in directory


def request_data(url, count=None):
    if count:
        print('count expected')
    logging.debug('request csv file')
    response = requests.get(url)
    logging.debug('response retrieved')
    # check status before report obout the response been success retrieved
    if response.ok:
        logging.debug('response status - success')
        return response.text
    else:
        return ('request failed' + str(response.status_code))


def to_json(input_file, output_file):
    """format csv file to json format"""

    # open both files with needed permissions
    csv_file = open(input_file, 'r')
    json_file = open(output_file, 'w')

    # read csv datax
    reader = csv.DictReader(csv_file, restkey=None, restval=None)
    # write the csv data into json file but previously format it to json
    json_file.write(json.dumps([entry for entry in reader],
                               indent=int(4 if config['PRETTY'] else 0)))  # prettify constant example of use

    csv_file.close()
    json_file.close()


if __name__ == "__main__":
    if config['CACHED']:
        data = request_data(config['URL'])
        cache['cached_data'] = data
    try:
        if is_file_local(sys.argv[1]):
            to_json(sys.argv[1], config['JSON_'])
            print('yes, find it')
        else:
            to_json(config['CSV_'], config['JSON_'])
            print('provide localy placed file to work with')
    except ValueError:
        print(
            """
            provide input and output file as commandline arguments
            here is the link on github repo, https://github.com/whoami911329/python-csv-to-json-formater
            where yo can find most of documentation. 
            """
        )
