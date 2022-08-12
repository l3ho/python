import os
import sys
import re
import csv
from random import randrange
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'gui'))
from tkinter import *
from multi_test import main
from mailer import Message, connect_to_mailbox, HTMLBody, FileAttachment
from utils import get_reports_by_be, get_folder_name_by_date
from main import ExcelManager

parent_folder = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
REPORTS_FOLDER = os.path.join(parent_folder, 'reports')
LOG_FOLDER = os.path.join(parent_folder, 'log')
logfile = os.path.join(LOG_FOLDER, get_folder_name_by_date() + '.csv')

registers, report_be = get_reports_by_be(REPORTS_FOLDER)
print(registers)
print(report_be)

MAILBOXES = {
    'FLT': 'FLTmutabakat@pepsico.com',
    'FMS': 'FMSmutabakat@pepsico.com',
    'PCSD': 'PCSDmutabakat@pepsico.com'
}

root = Tk()
root.title('Zero Balance')
root.geometry('400x200')

user_mailbox_label = Label(root, text='User E-mail:', font=('arial', 9, 'bold')).place(x=10, y=10)
user_mailbox_value = StringVar(root, value='artem.moriashov1.contractor@pepsico.com')
user_mailbox_entry = Entry(root, textvariable=user_mailbox_value, width=60, bg='white').place(x=10, y=30)

user_gpid_label = Label(root, text='User GPID:', font=('arial', 9, 'bold')).place(x=200, y=50)
user_gpid_value = StringVar(root, value='09271848')
user_gpid_entry = Entry(root, textvariable=user_gpid_value, width=10, bg='white').place(x=200, y=70)

user_password_label = Label(root, text='User Password:', font=('arial', 9, 'bold')).place(x=10, y=50)
user_password_value = StringVar(root)
user_password_entry = Entry(root, show='*', textvariable=user_password_value, width=20, bg='white').place(x=10, y=70)


def run_main_script():
    try:
        account = connect_to_mailbox(user_mailbox_value.get(), user_password_value.get(), MAILBOXES[report_be])
    except:
        sys.exit('Cant get access of your mailbox. Please check the password.')

    register, quarter_data, output_folder_for_pdf = main()

    if not register:
        sys.exit('Vendors with zero balance were not found in the register')

    xls = ExcelManager(registers[report_be])

    print('Sending emails...')

    [os.remove(os.path.join(LOG_FOLDER, file)) for file in os.listdir(LOG_FOLDER)]

    f = open(logfile, 'a', newline='', encoding='utf-8', errors='replace')
    writer = csv.writer(f)
    
    for key, value in register.items():
        pdf_file = os.path.join(output_folder_for_pdf, key + '.pdf')
        if not os.path.exists(pdf_file):
            xls.set_value(f'E{value[-2]}', 'the file was not saved')
            continue
        
        new_name = '_'.join([register[key][-1], register[key][2], quarter_data[1], quarter_data[2]])
        new_name = re.sub(r'[\\/*<>]', '', new_name)
        new_file = os.path.join(output_folder_for_pdf, new_name + '.pdf')
        if os.path.exists(new_file):
            new_file = os.path.join(output_folder_for_pdf, new_name + '_' + str(randrange(100)) + '.pdf')
        os.rename(pdf_file, new_file)
        

        emails = re.findall(r'[\w.-]+@[\w.-]+', value[5])
        if value[5] != '' and not emails:
            xls.set_value(f'E{value[-2]}', 'the email was not specified')
            continue
        if emails:
            body = ''.join([
                'Merhaba,<br><br>',
                'Gönderdiğim mutabakat mektubuna kaşeli ve imzalı dönüşünüzü rica ediyoruz.<br><br>',
                'Şimdiden teşekkürler.<br><br>',
                'Saygilarimla<br><br>',
                'Mutabakat uzmani.'
                ])
            subject = new_name
            
            m = Message(
                account=account,
                folder=account.sent,
                subject=subject,
                body=HTMLBody(body),
                to_recipients=emails,
                )
            with open(new_file, 'rb') as f:
                content = f.read()
            m.attach(FileAttachment(name=new_name + '.pdf', content=content))

            m.send_and_save()
            xls.set_value(f'E{value[-2]}', 'sent')
            writer.writerow([str(subject), register[key][-1], register[key][2], quarter_data[1], quarter_data[2]])
    
    f.close()
    print('Emails were sent')
    xls.save(registers[report_be])

    print('Saving changes to report')

    print('Job is Done!!!')

        
    

run_mainbutton = Button(root, text='Run Script', width=10, height=2, bg='lightblue', command=run_main_script).place(x=10, y=95)


root.mainloop()