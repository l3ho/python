import sys
import os
import datetime
import re
from collections import Counter
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'site-packages'))

import xlrd

def get_report_data(xls, sheet_name=None):
    report = []
    wb = xlrd.open_workbook(xls)
    if sheet_name:
        sheet = wb.sheet_by_name(sheet_name)
    else:
        sheet = wb.sheet_by_index(0)
    for i in range(0, sheet.nrows)[2:]:
        row = sheet.row_values(rowx=i)
        if sheet_name == 'PO Receipts' and row[12] != '':
            irsalie = []
            irsalie_string = str(re.sub(r'[^\w-]', '', str(row[12])))
            if re.findall(r'-(\d+)', str(row[12])):     
                root = re.search(r'(\w+)-', irsalie_string).groups()[0]
                irsalie.append(root)
                tails = re.findall(r'-(\d+)', irsalie_string)
                for tail in tails:
                    irsalie.append(root[:-(len(tail))] + tail)
                
            else:
                irsalie.append(irsalie_string)
            row[12] = irsalie
        report.append(row)
    return report


def get_unique_po_from_report(report):
    fms_duplicate = [str(i[6]) for i in report]
    get_dupc = [k for k,v in Counter(fms_duplicate).items() if v>1]
    unique_po = set(fms_duplicate) - set(get_dupc)
    # print(len(fms_duplicate))
    return list(unique_po)

def compare_suppliers(supplier1, supplier2, use_blank=False):
    if use_blank:
        if supplier1 == '' or \
            supplier2 == '' or \
            'vendor master pending' in str(supplier1).lower() or \
            'vendor master pending' in str(supplier2).lower():
                # print(f'Comapre worked, supplier1 {supplier1}, supplier2{supplier2}')
                return True
    if len(supplier1) > 15 and len(supplier2) > 15:
        return supplier1[:15] == supplier2[:15]
    else:
        return supplier2 in supplier1

def check_suppliers_for_gib(supplier1, supplier2):
    if supplier1 == '' or supplier2 == '':
        return True
    if 'vendor master pending' in str(supplier1).lower() or 'vendor master pending' in str(supplier2).lower():
        return True

def check_report_folder(folder):
    if not os.path.exists(folder):
        sys.exit(f'Something wrong with report folder. Please check the path {folder}')


    reports_template = ['FMS', 'FLT', 'PCSD', 'INVOICE', 'MUBUY']

    grni_reports = {}


    files = os.listdir(folder)
    print(files)

    for report in reports_template:
        template_found = False
        for file in files:
            if report in str(file).upper() and file.endswith('xlsx'):
                grni_reports[report] = os.path.join(folder, file)

                template_found = True
        if not template_found:
            sys.exit(f'Seems like report {report} is missing')

    return grni_reports

user_report = {}

wb = xlrd.open_workbook('user_list.xlsx')
sheet = wb.sheet_by_name('LIST')
for i in range(0, sheet.nrows):
    row = sheet.row_values(rowx=i)
    user_report[row[0]] = row[3]





