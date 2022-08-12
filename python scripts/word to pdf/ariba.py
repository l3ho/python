import sys
import os
import datetime
import uuid
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'site-packages'))
import pywintypes
from docx import Document
from docx.shared import Pt

import win32com.client
from docx2pdf import convert

from subprocess import  Popen
LIBRE_OFFICE = r"\\smb.ukldcisilon01.cww.pep.pvt\TurkeyFinance\IBM-Pepsi_PTP\CI\Artem\utils\LibreOfficePortable\App\libreoffice\program\soffice.exe"


def create_pdf_name(parent_folder, be_name, vendor_name, quater_name, year):
    file_name = '_'.join([be_name, vendor_name, quater_name, year])
    return os.path.join(parent_folder, file_name + '.docx')

def word_proccess(word_templates, vendor_name, vendor_id, qends_date, word_temp_folder, item, be):
    document = Document(word_templates[be])
    for paragraph in document.paragraphs:
        if 'VENDOR_NAME_TEMPLATE' in paragraph.text:
            # print(paragraph.text)
            paragraph.text = paragraph.text.replace('VENDOR_NAME_TEMPLATE', vendor_name)
            paragraph.style.font.name = 'Albany WT J'
            paragraph.style.font.size = Pt(14)
        elif 'VENDOR_ID_TEMPLATE' in paragraph.text:
            # print(paragraph.text)
            paragraph.text = paragraph.text.replace('VENDOR_ID_TEMPLATE', vendor_id)
            paragraph.style.font.name = 'Albany WT J'
            paragraph.style.font.size = Pt(14)
        elif 'DATE_TEMPLATE' in paragraph.text:
            # print(paragraph.text)
            paragraph.text = paragraph.text.replace('DATE_TEMPLATE', qends_date[0])
            paragraph.style.font.name = 'Albany WT J'
            paragraph.style.font.size = Pt(14)
    output_file = os.path.join(word_temp_folder, str(item) + '.docx')
    document.save(output_file)
    return output_file

def word_multiproccessing(item, register_dict, word_temp_folder, qends_date, word_templates):
    file = word_proccess(word_templates, register_dict[item][2], register_dict[item][1], qends_date, word_temp_folder, item, register_dict[item][-1])
    return file




def convert_to_pdf(temp, out_folder, files):
    p = Popen([LIBRE_OFFICE, '--headless', '--convert-to', 'pdf', '--outdir',
               out_folder] + [os.path.join(temp, file) for file in files])
    # print([LIBRE_OFFICE, '--convert-to', 'pdf', input_docx])
    p.communicate()
