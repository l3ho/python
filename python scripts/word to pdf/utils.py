import sys
import os
import re
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'mailer'))
import datetime


def get_folder_name_by_date():
    return datetime.datetime.today().strftime('%d-%m-%Y')

def mkdir_for_pdfs(parent_folder, date):
    path = os.path.join(parent_folder, date)
    if not os.path.exists(path): 
        os.mkdir(path)
    return path

def get_q_ends_date():
    month = datetime.datetime.today().month
    if 1 <= month <= 3:
        print('31-DEC-20')
        return '31-DEC-20', 'Q4', '2020'
    elif 4 <= month <= 6:
        print('31-MAR-21')
        return '31-MAR-21', 'Q1', '2021'
    elif 7 <= month <= 9:
        print('30-JUN-21')
        return '30-JUN-21', 'Q2', '2021'
    elif 10 <= month <= 12:
        print('30-SEP-21')
        return '30-SEP-21', 'Q3', '2021'


def get_reports_by_be(report_folder):
    be = ['FLT', 'FMS', 'PCSD']
    registers = {}
    for b in be:
        for file in os.listdir(report_folder):
            if b in file and str(file).upper().endswith('.XLSX'):
                registers[b] = os.path.join(report_folder, file)
    if len(registers) != 1:
        sys.exit('Either the report is missing or there are more than one in the folder or file\'s format is not XLSX')
    return registers, list(registers.keys())[0]


def split_list(folder, n):
    result = [os.listdir(folder)[i:i + n] for i in range(0, len(os.listdir(folder)), n)]
    return result

def get_email(string):
    emails = re.findall(r'[\w.-]+@[\w.-]+', string)
    return emails