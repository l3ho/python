import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'gui'))
from tkinter import *
from tkinter import messagebox
import datetime
import re

from setup import get_pdfs_in_input_folder, create_output_folder_with_date, get_text_from_digital_pdf, get_pdf_num_pages, extractPage

root = Tk()
root.title('PDF Cutter')
root.geometry('400x200')

labelframe = LabelFrame(root, text="Select the processing type", padx=5, pady=5, height=170, width=300)
labelframe.pack(fill="both", expand="yes")


def sel():
    if var.get() == 1:
        pdf_first_page_entry['state'] = 'disabled'
    else:
        pdf_first_page_entry['state'] = 'normal'


def main_script_func():
    files_to_process = get_pdfs_in_input_folder()
    print(files_to_process)
    if not files_to_process:
        raise ValueError('INPUT FOLDER IS EMPTY! PLEASE PUT PDF INSIDE TO BE PROCCESSED')

    output_folder = create_output_folder_with_date()

    for file in files_to_process:
        if var.get() == 1:
            get_pages_by_recognition = get_text_from_digital_pdf(file)
            extractPage(file, output_folder, get_pages_by_recognition.keys(), pdf_data=get_pages_by_recognition)

        else:
            try:
                user_input = pdf_first_page_value.get()
            except:
                raise ValueError('Please provide a number')

            pages = range(1, get_pdf_num_pages(file) + 1)
            extractPage(file, output_folder, pages, pdf_count=user_input)

    print('JOB IS DONE')









pdf_first_page_label = Label(labelframe, text='lenght of PDF:')
pdf_first_page_label.place(x=10, y=50)
pdf_first_page_value = IntVar(root, value='2')
pdf_first_page_entry = Entry(labelframe, textvariable=pdf_first_page_value, width=25)
pdf_first_page_entry.place(x=10, y=70)




var = IntVar(labelframe, 2)
R1 = Radiobutton(labelframe, text="Text Recognition", variable=var, value=1, command=sel)
R1.pack(anchor=W)

R2 = Radiobutton(labelframe, text="Based on lenght of pdf(Only 1st page)", variable=var, value=2, command=sel)
R2.pack(anchor=W)




run_script = Button(root, text='Run Script', width=10, height=2, bg='lightblue', command=main_script_func)
run_script.place(x=20, y=140)

root.mainloop()