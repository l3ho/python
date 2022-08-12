import sys
import os
import re
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'mailer'))
import datetime
from exchangelib import EWSTimeZone, EWSDateTime

def get_timezone(region=None):
    """get timezone by region. e.g(Europe/Moscow) or return local machine tz"""
    try:
        tz = EWSTimeZone.timezone(region)
        return tz
    except:
        tz = EWSTimeZone.localzone()
        return tz

def get_time_range(tz):

    right_now = tz.localize(EWSDateTime.now()).replace(day=1) - datetime.timedelta(days=1)
    start_range = right_now.replace(day=1)

    return start_range

def avoid_duplicate(filename):
    """add current time to a filename to prevent saving file with the same name"""
    head, tail = filename.rsplit('.', 1)
    filename = head + '_' + str(datetime.datetime.now())[:19].replace(":","_") + '.' + tail
    return filename

def split_filename(filename):
    """split file e.g Example.pdf to 'Example' and 'pdf'"""
    head, tail = filename.rsplit('.', 1)
    return head, tail

def be_recognition(filename, letters):
    
    head, tail = split_filename(filename)
    if re.search(r'[A-Z]{3}20\d{11}', filename.upper()) and tail.upper() == 'PDF':
        return letters['invoice']
    elif re.search(r'(FLT|FMS|PCSD)[-_]\d{5}', filename.upper()):
        return letters['form']
    else:
        return None

def get_po_num(po_num, attachement_name):
    if po_num in attachement_name:
        return po_num



