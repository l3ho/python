import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'site-packages'))
import datetime
import pdfplumber
import re
from PyPDF2 import PdfFileWriter, PdfFileReader

PARENT_FOLDER = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

INPUT_FOLDER = os.path.join(PARENT_FOLDER, 'input')
OUTPUT_FOLDER = os.path.join(PARENT_FOLDER, 'output')

def create_output_folder_with_date():
    path = os.path.join(OUTPUT_FOLDER, datetime.datetime.today().date().strftime('%d-%m-%Y'))
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_pdfs_in_input_folder():
    return list([os.path.join(INPUT_FOLDER, file) for file in os.listdir(INPUT_FOLDER) if file.upper().endswith('.PDF')])


def get_text_from_digital_pdf(file):
    pgs = dict()
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if 'Allianz Tower Küçükbakkalköy Mh. Kayışdağı Cd.No:1 34750' in text or 'Kayışdağı Cad. No:1 Ataşehir/İstanbul 34750' in text:
                numbers = re.search(r'^((\d{4}\s){4}).*?(\d.*?)\s', text, re.M | re.S)
                # re.search(r'^((\d{4}\s){4}).*NO:.*?((\d{4})|(\d+/\d+))', text, re.M | re.S)
                if numbers is not None:
                    pgs[page.page_number] = str(numbers.groups()[0]).replace(' ', '') + '-' + str(
                        numbers.groups()[2]).replace('/', '')

    return pgs

def extractPage(f, output_folder, pages: list, pdf_data: dict = None, pdf_count: int = None):
    file = open(f, 'rb')
    pdfOne = PdfFileReader(file, strict=False)
    counter = 1
    for page in pages:
        if pdf_count:
            if not (page + (pdf_count - 1)) % pdf_count == 0:
                continue
        output = PdfFileWriter()
        output.addPage(pdfOne.getPage(page - 1))
        if pdf_data:
            outputStream = open(os.path.join(output_folder, pdf_data[page] + '.pdf'), "wb")
        else:

            outputStream = open(os.path.join(output_folder, f'{os.path.split(f)[1][:-4]}-{str(counter)}.pdf'), "wb")
            counter += 1

        output.write(outputStream)
        outputStream.close()
    file.close()
    return

def get_pdf_num_pages(file):
    with pdfplumber.open(file) as pdf:
        return pdf.pages[-1].page_number

