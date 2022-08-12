import sys
import os
import re
import datetime
import time
import uuid
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'site-packages'))
import xlrd
import multiprocessing.dummy as multiprocessing
from functools import partial
from utils import get_folder_name_by_date, mkdir_for_pdfs, get_q_ends_date, get_reports_by_be, split_list, get_email
from ariba import word_proccess, convert_to_pdf, word_multiproccessing


def main():
    start = time.time()



    temp_folder = os.path.join(os.getcwd(), 'temp')
    [os.remove(os.path.join(temp_folder, file)) for file in os.listdir(temp_folder)]
    parent_folder = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    print(parent_folder)


    REPORTS_FOLDER = os.path.join(parent_folder, 'reports')

    registers, report_be = get_reports_by_be(REPORTS_FOLDER)

    print(registers)


    word_template_folder = os.path.join(parent_folder, 'word_templates')

    word_templates = {
        'FLT': os.path.join(word_template_folder, 'FLT.docx'),
        'FMS': os.path.join(word_template_folder, 'FMS.docx'),
        'PCSD': os.path.join(word_template_folder, 'PCSD.docx'),
    } 

    date_name = get_folder_name_by_date()
    output_folder_for_pdf = mkdir_for_pdfs(os.path.join(parent_folder, 'pdf'), date_name)

    quarter_data = get_q_ends_date()

    register = {}
    exceptions = []

    exception_file = os.path.join(parent_folder, 'exceptions' ,'exceptions.xlsx')

    wb = xlrd.open_workbook(exception_file)
    sheet = wb.sheet_by_index(0)
    for i in range(0, sheet.nrows)[1:]:
        row = sheet.row_values(rowx=i)
        row[0] = str(row[0]).replace('.0', '')
        exceptions.append(row[0])

    print('Exceptions are loaded')

    for be, reg in registers.items():
        print(be)
        wb = xlrd.open_workbook(reg)
        sheet = wb.sheet_by_name('GL Cari Hesap Ekstresi 100%')
        for i in range(0, sheet.nrows):
            row = sheet.row_values(rowx=i)[:10]
            if str(row[3]) == '0.0' and \
                    str(row[6]) == '' and \
                    str(row[7]) == '' and \
                    str(row[8]) == '' and \
                    str(row[9]) == '' and \
                    get_email(str(row[5])) and \
                    str(row[1]).replace('.0', '') not in exceptions:
                row[0] = str(row[0]).replace('.0', '')
                row[1] = str(row[1]).replace('.0', '')
                row.append(str(i + 1))
                row.append(be)
                # print(row)
                register[str(uuid.uuid4())] = row


    print('Register is loaded')
  


    p = multiprocessing.Pool()
    word_proccessing = partial(word_multiproccessing, register_dict=register, word_temp_folder=temp_folder, qends_date=quarter_data, word_templates=word_templates)
    word_proccessing = p.map(word_proccessing, register)
    p.close()
    p.join()

    print(len(register))

    print('Words files were created')

    splitted_files = split_list(temp_folder, 200)
    for i in splitted_files:
        print(len(i))
        convert_to_pdf(temp_folder, output_folder_for_pdf, i)


    print('Pdf files were converted')

    print(time.time() - start)
    return register, quarter_data, output_folder_for_pdf
