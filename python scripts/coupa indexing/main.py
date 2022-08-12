import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'gui'))
from chrome_am import get_xls_eportal, asyncio, get_invoices_coupa_web, main_func
from tkinter import *
from tkinter import messagebox
import datetime
import re

root = Tk()
root.title('Coupa AutoIndexing')
root.geometry('400x400')

labelframe = LabelFrame(root, text="Have E-Portal xls?", padx=5, pady=5, height=300, width=300)
labelframe.pack(fill="both", expand="yes")

coupa_frame = LabelFrame(root, text='Coupa part', padx=5, pady=5, height=100, width=300)
coupa_frame.pack(fill='both', expand='yes')

def sel():
    if var.get() == 1:
        eportal_login_entry['state'] = 'disabled'
        eportal_password_entry['state'] = 'disabled'
        start_date_entry['state'] = 'disabled'
        end_date_entry['state'] = 'disabled'
        gpid_entry['state'] = 'disabled'
    else:
        eportal_login_entry['state'] = 'normal'
        eportal_password_entry['state'] = 'normal'
        start_date_entry['state'] = 'normal'
        end_date_entry['state'] = 'normal'
        gpid_entry['state'] = 'normal'


def main_script_func():
    dwnl_folder = f'C:\\Users\\{gpid_value.get()}\\Downloads'
    #dwnl_folder = f'C:\\Users\\pl77906\\Desktop\\coupa_att'

    if var.get() == 2:
        print('gpid - ', gpid_value.get())       
        print('eportal login - ', eportal_login_value.get())
        print('start date is -', start_date_value.get())
        print('end date is -', end_date_value.get())
        if eportal_password_value.get() == '':
            return messagebox.showerror("Error", "please fill password field")
        if not re.search(r'(?:\d{2}\.){2}\d{4}', start_date_value.get()) or not re.search(r'(?:\d{2}\.){2}\d{4}', end_date_value.get()):
            return messagebox.showerror("Error", "Date format is incorrect")
        [os.remove(os.path.join(dwnl_folder, file)) for file in os.listdir(dwnl_folder) if 'InvoiceGrid' in file]
        asyncio.get_event_loop().run_until_complete(get_xls_eportal(eportal_login_value.get(), eportal_password_value.get(), start_date_value.get(), end_date_value.get(), dwnl_folder))  
    
    if coupa_password_value.get() == '':
        return messagebox.showerror("Error", "Coupa Password is not defined")

    count_xls_from_eportal = len([i for i, filename in enumerate(os.listdir(dwnl_folder)) if 'InvoiceGrid' in filename])
    # if count_xls_from_eportal != 6:
    #     messagebox.showwarning("Warning!", "Please check number of E-Portal xls files")
    
    invoices_on_page = asyncio.get_event_loop().run_until_complete(get_invoices_coupa_web(coupa_login_value.get(), coupa_password_value.get()))
    asyncio.get_event_loop().run_until_complete(main_func(coupa_login_value.get(), coupa_password_value.get(), dwnl_folder, invoices_on_page))
    print('Job Is Done')

eportal_login_label = Label(labelframe, text='E-Portal login:')
eportal_login_label.place(x=10, y=50)
eportal_login_value = StringVar(root, value='123987')
eportal_login_entry = Entry(labelframe, textvariable=eportal_login_value, width=25)
eportal_login_entry.place(x=10, y=70)

eportal_password_label = Label(labelframe, text='E-Portal Password:')
eportal_password_label.place(x=10, y=90)
eportal_password_value = StringVar(root)
eportal_password_entry = Entry(labelframe, show='*', textvariable=eportal_password_value)
eportal_password_entry.place(x=10, y=110)

gpid_label = Label(labelframe, text='GPID:')
gpid_label.place(x=200, y=10)
gpid_value = StringVar(root, value='09145375')
gpid_entry = Entry(labelframe, textvariable=gpid_value)

print(gpid_value)
gpid_entry.place(x=200, y=27)

start_date_label = Label(labelframe, text='Start Date(e.g 03.12.2019):')
start_date_label.place(x=200, y=50)
start_date_value = StringVar(labelframe, value=(datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%d.%m.%Y"))
start_date_entry = Entry(labelframe, textvariable=start_date_value)
start_date_entry.place(x=200, y=70)

end_date_label = Label(labelframe, text='End Date(e.g 03.12.2019):')
end_date_label.place(x=200, y=90)
end_date_value = StringVar(labelframe, value=datetime.datetime.today().strftime("%d.%m.%Y"))
end_date_entry = Entry(labelframe, textvariable=end_date_value)
end_date_entry.place(x=200, y=110)

var = IntVar(labelframe, 2)
R1 = Radiobutton(labelframe, text="Yes", variable=var, value=1, command=sel)
R1.pack(anchor=W)

R2 = Radiobutton(labelframe, text="No", variable=var, value=2, command=sel)
R2.pack(anchor=W)

coupa_login_label = Label(coupa_frame, text='Coupa Login(IBM email):')
coupa_login_label.place(x=10, y=5)
coupa_login_value = StringVar(coupa_frame, value='Kamilla.Davletshina@ibm.com')
coupa_login_entry = Entry(coupa_frame, textvariable=coupa_login_value, width=30)
coupa_login_entry.place(x=10, y=25)

coupa_password_label = Label(coupa_frame, text='Coupa Password:')
coupa_password_label.place(x=10, y=45)
coupa_password_value = StringVar(coupa_frame)
coupa_password_entry = Entry(coupa_frame, textvariable=coupa_password_value, width=30, show='*')
coupa_password_entry.place(x=10, y=65)


run_script = Button(root, text='Run Script', width=10, height=2, bg='lightblue', command=main_script_func)
run_script.place(x=20, y=320)

root.mainloop()