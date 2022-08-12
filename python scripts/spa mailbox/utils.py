import sys
import os
import re
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'mailer'))
import datetime

def check_attach_for_pdf(item):
    for attachment in item.attachments:
        if attachment.name.upper().endswith('.PDF'):
            return True


def check_mail_size(item):
    limit = 10485760
    counter = 0
    for attachment in item.attachments:
        counter += attachment.size

    if counter > limit:
        return False
    else:
        return True

reply_body_mail_size_error = ''.join(['<html><head><meta charset="UTF-8"></head><body>Merhaba,<br><br>',
    'Mailinizde eklerin hacimi 10 mb’I astigi icin mailiniz isleme alinamadi. Control edip tekrar gondermenizi rica ederim.<br><br></body></html>'])

reply_body = ''.join(['<html><head><meta charset="UTF-8"></head><body>Merhaba,<br><br>',
                'Cagriniz islenemiyor. Sebebi: PDF formatinda ek fatura yok.<br><br>',
                'Lutfen PDF formatli fatura goruntusunu ekleyip tekrak mail gonderin.<br>',
                'Fatura girisiyle baska sorulariniz varsa, lutfen AP ekibine yazin.<br><br>',
                'Bu yanit otomatik yapilmistir, buraya donus yapmayiniz.</body></html>'])
