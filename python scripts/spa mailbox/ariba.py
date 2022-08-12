import sys
import os
working_directory = os.getcwd()
sys.path.append(os.path.join(working_directory, 'Lib', 'mailer'))
from exchangelib import Credentials, Account, Configuration, DELEGATE, FileAttachment, Message,\
                        EWSTimeZone, EWSDateTime

def connect_to_mailbox(user_mailbox, user_pass, smpt_address=None):
    if not smpt_address:
        smpt_address = user_mailbox
    server = r'outlook.office365.com'
    credentials = Credentials(user_mailbox, user_pass)
    config = Configuration(server=server, credentials=credentials)
    account = Account(primary_smtp_address=smpt_address, config=config, autodiscover=False, access_type=DELEGATE)

    ews_url = account.protocol.service_endpoint
    ews_auth_type = account.protocol.auth_type
    primary_smtp_address = account.primary_smtp_address

    config = Configuration(service_endpoint=ews_url, credentials=credentials, auth_type=ews_auth_type)
    account = Account(
        primary_smtp_address=primary_smtp_address, 
        config=config, autodiscover=False, 
        access_type=DELEGATE,
    )
    return account