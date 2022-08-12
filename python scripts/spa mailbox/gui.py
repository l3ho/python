import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'gui'))
from tkinter import *
from tkinter import messagebox
import datetime
import re
from utils import check_attach_for_pdf, reply_body, check_mail_size, reply_body_mail_size_error
from ariba import connect_to_mailbox
from exchangelib import Credentials, Account, Configuration, DELEGATE, FileAttachment, Message,\
                        EWSTimeZone, EWSDateTime, HTMLBody


COUPA_MAILBOX = 'invoices@pepsico.coupahost.com'

MAILBOX_EXCEPTIONS = ['do_not_reply@pepsico-test.coupahost.com', 
    'do_not_reply@pepsico.coupahost.com', 
    'invoices@pepsico-test.coupahost.com',
    'invoices@pepsico.coupahost.com']

ADDRESSES = ['FLTearsiv@pepsico.com', 'FMSearsiv@pepsico.com', 'PCSDearsiv@pepsico.com']


root = Tk()
root.title('Coupa AutoIndexing')
root.geometry('400x200')

labelframe = LabelFrame(root, text="Webmail Login", padx=5, pady=5, height=100, width=100)
labelframe.pack(fill="both", expand="yes")



def main_script_func():
    user_mailbox = str(eportal_login_value.get())
    


    # logging to mailbox


    for address in ADDRESSES:
        try:
            account = connect_to_mailbox(str(user_mailbox).strip(), str(eportal_password_value.get()).strip(), address)
        except:
            sys.exit('Seems like mail pwd is incorrect')

        coupa_folder = account.inbox / 'to Coupa'


        for item in account.inbox.all().only('id', 'changekey', 'attachments', 'subject', 'datetime_received', 'is_read', 'sender').iterator():
            if item.is_read is False and item.sender not in MAILBOX_EXCEPTIONS and 'AUTOMATIC REPLY' not in str(item.subject).upper():
                print(str(item.sender))
                print(str(item.subject))
                if check_attach_for_pdf(item):
                    if not check_mail_size(item):
                        reply = item.create_reply(subject='RE: ' + str(item.subject), body=HTMLBody(reply_body_mail_size_error), to_recipients=[item.sender]).save(account.drafts)
                        item.is_read = True
                        item.save()
                        reply.send()
                        continue
                    
                    item.move(coupa_folder)
                    forward = item.create_forward(subject='Fwd: ' + str(item.subject), body=HTMLBody(''), to_recipients=[COUPA_MAILBOX])
                    item.is_read = True
                    item.save()
                    forward.send()

                else:
                    # print('reply on ', item.subject)
                    try:
                        reply = item.create_reply(subject='RE: ' + str(item.subject), body=HTMLBody(reply_body), to_recipients=[item.sender]).save(account.drafts)
                    except:
                        continue
                    item.is_read = True
                    item.save()
                    reply.send()
        print(f'mailbox {address} successfully scanned')
    print('Job is Done')



eportal_login_label = Label(labelframe, text='E-mail:')
eportal_login_label.place(x=10, y=10)
eportal_login_value = StringVar(root, value='artem.moriashov1.contractor@pepsico.com')
eportal_login_entry = Entry(labelframe, textvariable=eportal_login_value, width=40)
eportal_login_entry.place(x=10, y=30)

eportal_password_label = Label(labelframe, text='E-mail Password:')
eportal_password_label.place(x=10, y=50)
eportal_password_value = StringVar(root)
eportal_password_entry = Entry(labelframe, show='*', textvariable=eportal_password_value)
eportal_password_entry.place(x=10, y=70)



run_script = Button(root, text='Run Script', width=10, height=2, bg='lightblue', command=main_script_func)
run_script.place(x=20, y=130)

root.mainloop()