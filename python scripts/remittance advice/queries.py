import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'site-packages'))
import cx_Oracle

dsn_tns = cx_Oracle.makedsn('30.201.196.181', '1563', service_name='TRQA')
conn = cx_Oracle.connect(user=r'', password='', dsn=dsn_tns)

c = conn.cursor()


def get_invoices_from_checks_all(vendors_ids, input_date, c):
    a = c.execute(f"""SELECT ACA.AMOUNT, ACA.CHECK_DATE, ACA.CHECK_ID, ACA.CHECKRUN_NAME, ACA.ORG_ID, ACA.VENDOR_ID, APS.SEGMENT1 FROM \
        AP.AP_CHECKS_ALL ACA \
        INNER JOIN (SELECT VENDOR_ID, SEGMENT1 FROM AP.AP_SUPPLIERS WHERE SEGMENT1 IN ({vendors_ids})) APS \
        ON ACA.VENDOR_ID = APS.VENDOR_ID \
        WHERE trunc(ACA.CHECK_DATE) = to_date('{input_date}', 'DD.MM.YYYY') AND CHECKRUN_NAME LIKE 'RUSLAN_%'""")
    return a

def get_invoices_from_all(check_id, supplier_id, c):
    a = c.execute(f"""SELECT AIPA.AMOUNT, AIA.INVOICE_NUM, AIPA.ORG_ID FROM AP.AP_INVOICE_PAYMENTS_ALL AIPA \
        LEFT JOIN AP.AP_INVOICES_ALL AIA \
        ON AIPA.INVOICE_ID = AIA.INVOICE_ID \
        WHERE AIPA.CHECK_ID = {check_id} AND AIPA.REMIT_TO_SUPPLIER_ID = {supplier_id}""")
    return a

