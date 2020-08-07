""" This is file converter module .
It reads csv file and generate json file
"""
import csv
import copy
import json
import logging
import argparse

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

core_attribute = {1: 'label', 2: 'Id', 0: 'link'}
length = len(core_attribute)

level_dict = {}


def read_and_clean_file(filename: str, delimiter: str,
                        skip_header: int, skip_columns: int) -> list:
    """
        load file into list of list , excluding no. of rows and columns are
        passed as skip_header and skip_columns. It also exclude empty rows.
    """
    tab_row_cols = []
    with open(filename) as csv_fp:
        file_reader = csv.reader(csv_fp, delimiter=delimiter)
        cntr = 0
        for line in file_reader:
            if cntr < skip_header:
                cntr = cntr + 1
                continue
            if not ''.join(line):
                continue
            tab_row_cols.append(line[skip_columns::])
    return tab_row_cols


def element_name(column_no: int) -> str:
    """ lookup for core attributes"""
    key = column_no % length
    return core_attribute.get(key)


def get_node_with_level(row: list) -> dict:
    """derives value label ,id and link for given row along with
       its level in the hierarchy"""
    log.info('get_node_with_level')
    sub_data = {'label': '', 'Id': '', 'link': ''}
    col_no = 0
    for item in row:
        col_no = col_no + 1
        if bool(item):
            key = element_name(col_no)
            sub_data[key] = item
        else:
            break
    if col_no < length:
        col_no = col_no - 1
    level = col_no / length
    sub_data['level'] = int(level)
    return sub_data


def add_node(row: list, main_data_list: list) -> None:
    """node is added as per the level in the dict tree hierarchy """
    log.info('add node')
    sub_data = get_node_with_level(row)
    level = sub_data['level']
    sub_data.popitem()
    sub_data['children'] = []
    log.debug('sub_data : %s', sub_data)
    if level == 1:
        # parent or root node
        level_dict[level] = sub_data['children']
        main_data_list.append(copy.copy(sub_data))
    else:
        # each dictionary maintain the reference of last children node added as per the level
        level_dict[level] = level_dict[level - 1]
        log.debug('level_dict[level] : %s', level_dict[level])
        log.debug('level_dict[level-1] : %s', level_dict[level - 1])
        level_dict[level].append(copy.copy(sub_data))
        level_dict[level] = sub_data['children']


def build_tree(row_tables: list, main_data_list: list) -> None:
    """nodes are nested in dictornary object """
    log.info('build_tree')
    no_of_cols = len(row_tables[1])
    log.info('intializing dictionary for each level with list')
    for c in range(0, no_of_cols, length):
        level = int(c / length) + 1
        level_dict[level] = []
    log.info('adding node to dictonary tree based on its heirarchy')
    for row in row_tables:
        add_node(row, main_data_list)


def convert_csv_to_json(ip_filename: str, delimiter: str,
                        skip_header: int, skip_columns: int, op_filename):
    """convert given csv file into json file
        :parameter
            ip_filename : csv filename
            delimiter : single character delimiter
            skip_header : number to exclude header rows
            skip_columns: number to exclude columns which are not part of json
     """

    try:
        log.info('reading csv file')
        main_data_list = []
        row_tables = read_and_clean_file(ip_filename, delimiter, skip_header, skip_columns)
        log.info('building dictonary with children')
        build_tree(row_tables, main_data_list)
        with open(op_filename, 'w') as json_fp:
            json_fp.write(json.dumps(main_data_list, indent=4))
        log.info('csv successfully converted to json')
    except FileNotFoundError:
        logging.error('csv file missing.please place it and rerun')
    except Exception:
        logging.error('Something has caused error', exc_info=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_filename', help="csv filename")
    parser.add_argument('delimiter', help="file delimiter in csv file for instance ,")
    parser.add_argument('skip_header', help="number of rows to be skipped .For instance to skip header row pass 1",
                        type=int)
    parser.add_argument('skip_columns',
                        help="number of columns to be skipped not part of hierarchy. for instance pass 1 ", type=int)
    parser.add_argument('op_filename', help="output file name for instance filename.json")
    args = parser.parse_args()
    convert_csv_to_json(args.ip_filename, args.delimiter, args.skip_header, args.skip_columns, args.op_filename)
