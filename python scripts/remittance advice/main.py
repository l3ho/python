import sys
import os
import re
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'gui'))
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'site-packages'))
from tkinter import *
from tkinter import messagebox

BASE_DIR = os.getcwd()
from utils import parse_vendor_list_xlsx, convert_vendor_ids_for_oracle_q, connect_to_mailbox, create_xlsx, Message, HTMLBody, FileAttachment
from queries import c, get_invoices_from_checks_all, get_invoices_from_all

BE = {
    82: 'FLT',
    83: 'PCSD',
    84: 'FMS',
}


PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

TEMP_FOLDER = os.path.join(BASE_DIR, 'temp')

[os.remove(os.path.join(TEMP_FOLDER, file)) for file in os.listdir(TEMP_FOLDER)]


vendor_list_forder = os.path.join(PARENT_DIR, 'Vendor list')

vendor_list_xlsx = os.path.join(vendor_list_forder, 'Vendor_list.xlsx')

vendors = parse_vendor_list_xlsx(vendor_list_xlsx)
print(vendors)

ids_for_oracle = convert_vendor_ids_for_oracle_q(vendors)
print(ids_for_oracle)





root = Tk()
root.title('Coupa AutoIndexing')
root.geometry('400x200')

labelframe = LabelFrame(root, text="Webmail Login", padx=5, pady=5, height=100, width=100)
labelframe.pack(fill="both", expand="yes")



def main_script_func():
    input_date = str(date_value.get())
    if not re.match(r'\d{2}.\d{2}.\d{4}', input_date):
        print('Invalid date format')
        return -1
    print(input_date)
    # sys.exit()    
    
    user_mailbox = str(eportal_login_value.get())

    try:
        account = connect_to_mailbox(user_mailbox, str(eportal_password_value.get()))
    except:
        sys.exit('Seems like mail pwd is incorrect')

    checks = get_invoices_from_checks_all(ids_for_oracle, input_date, c)

    checks_data = checks.fetchall()

    if not checks_data:
        print('Nothing found in Oracle DB')
        return -1

    for i in checks_data:

        if i[4] in vendors[int(i[-1])]['be']:
            print('CHECKED INVOICE ', i)
            invoices = get_invoices_from_all(i[2], i[-2], c)
            invoices_data = invoices.fetchall()
            if not invoices_data:
                continue
                

            xlsx_file = create_xlsx(invoices_data, TEMP_FOLDER, input_date)
            body = ''.join([
                'Merhaba,<br><br>',
                'Ödeme detaylarını ekte bulabilirsiniz.<br><br>',
                f'{BE[i[-3]]}.<br><br>',
                ])
    

            m = Message(
                        account=account,
                        folder=account.sent,
                        subject='Ödeme detaylarını',
                        body=HTMLBody(body),
                        to_recipients=[user_mailbox],)

            with open(xlsx_file, 'rb') as f:
                content = f.read()
            m.attach(FileAttachment(name='Ödeme detaylarını.xlsx', content=content))
            m.send_and_save()
    print('Job is Done')







eportal_login_label = Label(labelframe, text='E-mail:')
eportal_login_label.place(x=10, y=10)
eportal_login_value = StringVar(root, value='ruslan.salikhov@pepsico.com')
eportal_login_entry = Entry(labelframe, textvariable=eportal_login_value, width=40)
eportal_login_entry.place(x=10, y=30)

eportal_password_label = Label(labelframe, text='E-mail Password:')
eportal_password_label.place(x=10, y=50)
eportal_password_value = StringVar(root)
eportal_password_entry = Entry(labelframe, show='*', textvariable=eportal_password_value, width=20)
eportal_password_entry.place(x=10, y=70)

date_label = Label(labelframe, text='Date to be checked(eg 08.07.2021)')
date_label.place(x=160, y=50)
date_value = StringVar(root)
date_entry = Entry(labelframe, textvariable=date_value)
date_entry.place(x=160, y=70)



run_script = Button(root, text='Run Script', width=10, height=2, bg='lightblue', command=main_script_func)
run_script.place(x=20, y=130)

root.mainloop()
