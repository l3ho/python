import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'site-packages'))
import time
import asyncio
import re
import keyboard
import datetime
import csv
import collections
from pyppeteer import launch, errors
from bs4 import BeautifulSoup
from xls import list_of_invoices_eportal, get_exceptions_coupa
print('chrome_am libs are loaded')

current_date = datetime.datetime.today()

eportal_url = r'https://portal.digitalplanet.com.tr/login/index.html?returnUrl=/NetInvoice/Inbox.aspx'
coupa_url = r'https://pepsico.coupahost.com/invoices'


be_names = ['PCSD', 'FMS', 'FLT']

currency_list = {'USD': '1', 'GBP': '49', 'EUR': '46', 'TRY': '149', 'CHF': '29'}


async def get_xls_eportal(eportal_login, eportal_password, date_start, date_end, dwnl_folder):  
    for be_name in be_names:
        try:
            browser = await launch({'headless': True, 'executablePath': r'C:\Program Files\Google\Chrome\Application\chrome.exe'})
        except:
            browser = await launch({'headless': True, 'executablePath': r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'})
        context = await browser.createIncognitoBrowserContext()
        page = await context.newPage()
        await page.goto(eportal_url, {'waitUntil': 'domcontentloaded'})
        await page.waitForSelector('#txtCorporateCode')
        await page.type('#txtCorporateCode', be_name)
        await page.type('#txtLoginName', eportal_login)
        await page.type('#txtLoginPassword', eportal_password)
        await page.click('#btnLogin')
        for i in range(0, 2):
            if i == 1:
                await page.goto(r'https://portal.digitalplanet.com.tr/NetInvoice/InboxDrafts.aspx', {'waitUntil': 'domcontentloaded'})
            await page.waitForSelector('#InvoiceFilterBeginDate_I')
            time.sleep(4)
            await page.mouse.click(338, 207, {'clickCount': 2})
            print('click')
            await page.click('#InvoiceFilterBeginDate_I', {'clickCount': 2})
            await page.type('#InvoiceFilterBeginDate_I', date_start)
            print('date entered')
            await page.click('#InvoiceFilterEndDate_I', {'clickCount': 2})
            await page.type('#InvoiceFilterEndDate_I', date_end)
            await page.click('#btnRefresh')
            try:
                await page.waitForSelector('#InvoiceGrid_DXDataRow0')
            except errors.TimeoutError:
                pass
            time.sleep(2)
            counter_invoice_grid = len([i for i, file in enumerate(os.listdir(dwnl_folder)) if 'InvoiceGrid' in file])
            expected_invoice_xlsx = 'InvoiceGrid ' + f'({counter_invoice_grid})' + '.xlsx' if counter_invoice_grid > 0 else 'InvoiceGrid.xlsx'       
            await page.click('#exportToXLSXButton_CD')      
            while not os.path.exists(os.path.join(dwnl_folder, expected_invoice_xlsx)):
                print('waiting for file')
                time.sleep(3)
            print('file has been downloaded')
        await browser.close()



async def get_invoices_coupa_web(coupa_login, coupa_password):
    try:
        browser = await launch({'headless': True, 'executablePath': r'C:\Program Files\Google\Chrome\Application\chrome.exe'})
    except:
        browser = await launch({'headless': True, 'executablePath': r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'})
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    await page.goto(coupa_url, {'waitUntil': 'networkidle0'})
    await page.type('#user_login', coupa_login)
    await page.type('#user_password', coupa_password)
    await page.click('#login_form > button')
    try:
        await page.waitForSelector('#invoice_header_filter')
        await page.select('#invoice_header_filter', '-117')
    except:
        sys.exit('Error. Seems like Coupa password is incorrect!')
    await page.click('#sfBtn_invoice_header')
    time.sleep(5)
    await page.waitForSelector('#invoice_header_tbody')

    invoices_on_page = []
    while True:
        invoice_page_body = await page.content()
        soup = BeautifulSoup(invoice_page_body, 'html.parser')
        random_attr = ['stripe_even coupa_datatable_row', 'stripe_odd coupa_datatable_row',
                       'stripe_even coupa_datatable_row selected']
        
        for attr in random_attr:
            find_elements_on_page = soup.find_all(class_=attr)
            for element in find_elements_on_page:
                if not element.find(class_='icon icon_button sprite-lock_blue'):
                    invoice_coupa_attr = re.findall(r'\w.*', element.get_text())
                    find_invoice_number = re.search(r'invoices/(\d+)', str(element.find('a', href=True))).groups(0)
                    invoice_coupa_attr.append(find_invoice_number[0])
                    invoices_on_page.append(invoice_coupa_attr)
        if soup.find(class_='next_page invoice_header_wait'):
            try:
                await page.click('.next_page')
                time.sleep(2)
            except:
                pass
        else:
            break
    invoices_on_page = set(tuple(row) for row in invoices_on_page)
    invoices_on_page = [list(row) for row in invoices_on_page if row[5] == 'New' and row[4] == '0.00' and row[0] != 'None']
    print('Invoices found for matching - ', len(invoices_on_page))
    await browser.close()
    return invoices_on_page


async def main_func(coupa_login, coupa_password, dwnl_folder, invoices_on_page):
    try:
        browser = await launch({'headless': True, 'executablePath': r'C:\Program Files\Google\Chrome\Application\chrome.exe'})
    except:
        browser = await launch({'headless': True, 'executablePath': r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'})
    context = await browser.createIncognitoBrowserContext()
    page_void = await context.newPage()
    await page_void.setViewport({'width': 1150, 'height': 750})
    await page_void.goto(r'https://pepsico.coupahost.com/invoices', {'waitUntil': 'domcontentloaded'})
    await page_void.type('#user_login', coupa_login)
    await page_void.type('#user_password', coupa_password)
    await page_void.click('#login_form > button')
    await page_void.waitForSelector('#invoice_header_filter')
    await page_void.select('#invoice_header_filter', '-130')


    edit_invoice_page = await context.newPage()
    await edit_invoice_page.setViewport({'width': 1150, 'height': 750})
    url_edit_invoice = r'https://pepsico.coupahost.com/reports'
    await edit_invoice_page.goto(url_edit_invoice, {'waitUntil': 'domcontentloaded'})
    
    find_supplier = await context.newPage()
    await find_supplier.setViewport({'width': 1150, 'height': 750})
    url_supplier = r'https://pepsico.coupahost.com/suppliers'
    await find_supplier.goto(url_supplier, {'waitUntil': 'domcontentloaded'})

    supplier_page = await context.newPage()
    await supplier_page.setViewport({'width': 1150, 'height': 750})
    await supplier_page.goto(url_supplier, {'waitUntil': 'domcontentloaded'})

    await edit_invoice_page.bringToFront()
    print(dwnl_folder)
    eportal_invoices = list_of_invoices_eportal(dwnl_folder)
    eportal_dupl = collections.Counter()
    for eportal_inv in eportal_invoices:
        eportal_dupl[eportal_inv[1]] += 1
    eportal_dupl_list = list(dict(filter(lambda x: x[1] > 1, dict(eportal_dupl).items())).keys())


    print(len(eportal_invoices))
    currency_list = {'USD': '1', 'GBP': '49', 'EUR': '46', 'TRY': '149', 'CHF': '29'}
    exceptions, exceptions_voiding = get_exceptions_coupa()
    exceptions_voiding = list(map(lambda x: x.upper(), exceptions_voiding))
    log_file = os.path.join(os.getcwd(), 'logs', str(datetime.datetime.today().strftime('%d.%m.%Y')) + '.csv')
    for invoice_coupa in invoices_on_page:
        for invoice_eportal in eportal_invoices:
            if invoice_coupa[0] == invoice_eportal[1]:
                f = open(log_file, 'a', newline='', encoding='utf-8', errors='replace')
                writer = csv.writer(f)                
                print('coupa invoice - ', invoice_coupa)
                print('eportal invoice - ', invoice_eportal)
                if invoice_coupa[0] in eportal_dupl_list:
                    writer.writerow([invoice_coupa[0], 'Duplicated'])
                    f.close()
                    print('****************************************************')
                    break           
# ['MİGROS TİCARET.A.Ş.', 'M082021000138908', '6220529513', 'TRY  ', '42.03', '', '08/04/21', 'D012021002774946']
                date = invoice_eportal[-2]
                currency = invoice_eportal[3].strip()
                po_number = str(invoice_eportal[-3]).strip()
                amount = invoice_eportal[4]
                supplier_name = invoice_eportal[0]
                balance_unit = invoice_coupa[2]
                irsaliye = str(invoice_eportal[-1]).strip()
                status = 'Error'
                if str(invoice_eportal[0]).upper() in exceptions.keys():
                    supplier_name = exceptions[invoice_eportal[0]]
                suppliers_found = []
                if supplier_name.upper() in exceptions_voiding:
                    suppliers_found.append('No Processing Required-' + balance_unit)

                await edit_invoice_page.goto(f'https://pepsico.coupahost.com/invoices/{invoice_coupa[-1]}/edit', {'waitUntil': 'domcontentloaded'})
                await edit_invoice_page.bringToFront()
                await edit_invoice_page.type('#invoice_local_invoice_date', date)
                await edit_invoice_page.keyboard.press('Enter')
                try:
                    await edit_invoice_page.select('#invoice_currency_id', currency_list[currency])
                except:
                    writer.writerow([invoice_coupa[0], 'Error', suppliers_found, supplier_name, amount])
                    print('FILE IS BUSY')
                    f.close()
                    print('****************************************************')
                    break
                if po_number != '':
                    await edit_invoice_page.type('#invoice_custom_field_5', po_number)

                if irsaliye != '':
                    await edit_invoice_page.type('#invoice_custom_field_7', irsaliye)

                while True:
                    edit_invoice_page_text = await edit_invoice_page.content()
                    if re.search(r'id="invoice_invoice_lines_attributes_(\d+)"', edit_invoice_page_text):
                        line_number = re.search(r'id="invoice_invoice_lines_attributes_(\d+)"', edit_invoice_page_text).groups(0)[0]
                        close_btn = await edit_invoice_page.querySelector('.invoiceLineIconHolder > a:nth-child(2)')
                        await close_btn.click()
                        time.sleep(1)
                    else:
                        break

                await edit_invoice_page.waitForSelector('#add_invoice_line')
                await edit_invoice_page.click('#add_invoice_line')
                time.sleep(1.5)

                while True:
                    edit_invoice_page_text = await edit_invoice_page.content()
                    if re.search(r'id="invoice_invoice_lines_attributes_(\d+)"', edit_invoice_page_text):
                        line_number = re.search(r'id="invoice_invoice_lines_attributes_(\d+)"', edit_invoice_page_text).groups(0)[0]
                        break


                await edit_invoice_page.type(f'#invoice_invoice_lines_attributes_{line_number}_description', '1')
                await edit_invoice_page.type(f'#invoice_invoice_lines_attributes_{line_number}_price', amount)
                await edit_invoice_page.click('#calculate_button')
                time.sleep(1)
                

                try:
                    if len(suppliers_found) == 0:
                        await find_supplier.bringToFront()
                        await find_supplier.click('#sf_supplier', {'clickCount': 3})
                        try:
                            supplier_name_cut = re.search(r'\S+\s+\S+', supplier_name).group()
                        except(AttributeError):
                            supplier_name_cut = supplier_name
                        await find_supplier.type('#sf_supplier', supplier_name_cut)
                        element = await find_supplier.querySelector('#sfBtn_supplier')
                        # print(element)
                        # element = await find_supplier.querySelector('#supplier_data_table_form_search > div.inside > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(6) > div > a')
                        await element.click()
                        
                        counter = 0
                        while True:
                            find_supplier_text = await find_supplier.content()
                            soup = BeautifulSoup(find_supplier_text, 'html.parser')
                            text = soup.find(id='supplier_basic_rem')
                            counter += 1
                            if supplier_name_cut == text.get_text():
                                break
                            if counter == 60:
                                raise ValueError

                        find_supplier_body = await find_supplier.content()
                        soup_find_supplier = BeautifulSoup(find_supplier_body, 'html.parser')
                        list_of_suppliers = []
                        for odds_even in ['stripe_even coupa_datatable_row', 'stripe_odd coupa_datatable_row', 'stripe_even coupa_datatable_row selected']:
                            a = soup_find_supplier.find_all(class_=odds_even)
                            for b in a:
                                supplier_card = []
                                # supplier_card.append(b.find('a').string)
                                for i, c in enumerate(b.find_all('td')):
                                    if i == 1:
                                        supplier_card[0] = c.find('a').string
                                    supplier_card.append(str(c.string).strip())
                                find_supplier_id = re.search(r'suppliers\/show\/(\d+)', str(b.find('a')['href'])).groups(0)
                                supplier_card.append(find_supplier_id[0])
                                list_of_suppliers.append(supplier_card)
                        list_of_suppliers = [item for item in list_of_suppliers if item[3] == balance_unit and item[4] == 'Active']
                        print(list_of_suppliers)
                        find_inter = set()
                        [find_inter.add(l[2]) for l in list_of_suppliers]
                        for supplier in list_of_suppliers:
                            await supplier_page.goto(f'https://pepsico.coupahost.com/suppliers/show/{supplier[-1]}', {'waitUntil': 'domcontentloaded'})
                            html_supplier_card = await supplier_page.content()
                            soup_suppl = BeautifulSoup(html_supplier_card, 'html.parser')
                            get_tax_id_string = soup_suppl.find_all('div', class_='inline_form_element')[10].get_text()
                            try:
                                tax_id = re.search('\d+', get_tax_id_string).group()
                            except(AttributeError):
                                continue
                            print(tax_id)
                            if tax_id == invoice_eportal[2]:
                                suppliers_found.append(supplier)
                            if len(find_inter) == 1 and len(suppliers_found) > 0:
                                break
                                                   
                        if any('3-way' == x[2] for x in suppliers_found) and any('2-way' in x[2] for x in suppliers_found):
                            print('cant clarify supplier match level')

                        print('SUPPLIERS FOUND - ', suppliers_found)

                    
                    await edit_invoice_page.bringToFront()                    
                    if len(suppliers_found) == 1 and 'No Processing Required-' + balance_unit not in suppliers_found:
                        doc_type_exceptions_3way = ['SUPERONLINE ILETISIM HIZMETLER-2219-BIS-MYB-TUR-FLT',
                                                'SUPERONLINE ILETISIM HIZMETLER-1489366-NODEPT-MYB-TUR-FMS',
                                                'TT MOBIL ILETISIM HIZMETLERI A-4692379-NODEPT-ORA-TUR-PCSD'
                                                ]
                        doc_type_exceptions_2way = ['GOLDENBAY TURIZM YATIRIM A.S.-2275-NOWF-MYB-TUR-FLT',
                                      'GOLDENBAY TURIZM YATIRIM A.S.-3807-NOWF-MYB-TUR-FMS',
                                      'GOLDENBAY TURIZM YATIRIM A.S.-5186-NOWF-MYB-TUR-PCSD',
                                      'EGENCIA BUSINESS TRAVEL EXPEDI-367367-NODEPT-ORA-TUR-FLT',
                                      'EGENCIA BUSINESS TRAVEL EXPEDI-2309371-NODEPT-ORA-TUR-FMS',
                                      'EGENCIA BUSINESS TRAVEL EXPEDI-2309372-NODEPT-ORA-TUR-PCSD',
                                      'YUSEN INCI LOJISTIK VE TICARET-3218378-NODEPT-MYB-TUR-FLT',
                                      'YUSEN INCI LOJISTIK VE TICARET-3218379-NODEPT-MYB-TUR-FMS',
                                      'YUSEN INCI LOJISTIK VE TICARET-3218380-NODEPT-MYB-TUR-PCSD',
                                      'PINAPS ORG.VE KONGRE HIZMETLER-1326-NODEPT-MYB-TUR-FLT',
                                      'PINAPS ORG.VE KONGRE HIZMETLER-4684-NODEPT-MYB-TUR-PCSD',
                                      'PINAPS ORG.VE KONGRE HIZMETLER-1461013-NODEPT-MYB-TUR-FMS',
                                      'KARIYER NET ELEKTRONIK YAYIN V-1966-HR-MYB-TUR-FLT']
                        await edit_invoice_page.type('#invoice_supplier_search', suppliers_found[0][0])
                        await edit_invoice_page.keyboard.press('ArrowDown')
                        await edit_invoice_page.keyboard.press('Enter')
                        if suppliers_found[0][2] == '3-way'and suppliers_found[0][0] not in doc_type_exceptions_3way:
                            doc_type = 'SYSTEMPO_INVOICE'
                            billing_type = 'NOWF-NoWorkflowNeeded'
                        if suppliers_found[0][2] == '2-way' and suppliers_found[0][0] not in doc_type_exceptions_2way:
                            doc_type = 'NONPO_INVOICE'
                            billing_type = 'NODEPT'
                        if suppliers_found[0][0] in doc_type_exceptions_2way:
                            doc_type = 'NONPO_INVOICE'
                            billing_type = 'NOWF-NoWorkflowNeeded'
                        if suppliers_found[0][0] in doc_type_exceptions_3way:
                            doc_type = 'SYSTEMPO_INVOICE'
                            billing_type = 'NODEPT'
                        
                        ##################################################
                        counter = 0
                        while True:
                            await edit_invoice_page.click(f'#invoice_invoice_lines_attributes_{line_number}_account', {'clickCount': 4})
                            await edit_invoice_page.type(f'#invoice_invoice_lines_attributes_{line_number}_account', billing_type)
                            time.sleep(1.5)
                            await edit_invoice_page.keyboard.press('ArrowDown')
                            await edit_invoice_page.keyboard.press('Enter')
                            page_text = await edit_invoice_page.content()
                            soup = BeautifulSoup(page_text, 'html.parser')
                            get_billing_type = soup.find(id=f'invoice_invoice_lines_attributes_{line_number}_account')
                            counter += 1
                            if billing_type == get_billing_type.get_text():
                                break
                            popup_btn = False
                            if counter == 2:
                                await edit_invoice_page.click(f'#invoice_invoice_lines_attributes_{line_number}_account_account_picker_popup_button')
                                time.sleep(0.5)
                                await edit_invoice_page.waitForSelector('#account_segment_1_lv_id')
                                time.sleep(0.5)
                                if billing_type != 'NOWF-NoWorkflowNeeded':
                                    await edit_invoice_page.click('#account_segment_1_lv_id_chosen')
                                    time.sleep(0.5)
                                    await edit_invoice_page.keyboard.press('ArrowUp')
                                    time.sleep(0.5)
                                    await edit_invoice_page.keyboard.press('Enter')

                                time.sleep(1)
                                await edit_invoice_page.waitForSelector(f'#invoice_invoice_lines_attributes_{line_number}_account_picker_table_wrapper > div.spiffyTable.dataTable > div.head.picker_search.dynamic-picker > div.page_buttons_right > a')
                                await edit_invoice_page.click(f'#invoice_invoice_lines_attributes_{line_number}_account_picker_table_wrapper > div.spiffyTable.dataTable > div.head.picker_search.dynamic-picker > div.page_buttons_right > a')
                                time.sleep(2)
                                picker_window = 0
                                while True:
                                    page_text = await edit_invoice_page.content()
                                    soup = BeautifulSoup(page_text, 'html.parser')
                                    picker_window += 1
                                    if soup.find(id=f'invoice_invoice_lines_attributes_{line_number}_account_picker_table_wrapper') and picker_window < 3:
                                        time.sleep(2)
                                        print('windows is open')
                                    else:
                                        time.sleep(2)
                                        break
                                await edit_invoice_page.waitForSelector(f'#invoice_invoice_lines_attributes_{line_number}_account > span > span')
                                counter_after_btn_choose = 0
                                while True:
                                    page_text = await edit_invoice_page.content()
                                    soup = BeautifulSoup(page_text, 'html.parser')
                                    get_billing_type = soup.find('span', class_='hover_target billingHoverSpec')
                                    print(get_billing_type)
                                    counter_after_btn_choose += 1
                                    print(billing_type)
                                    if get_billing_type:
                                        if billing_type == get_billing_type.get_text():
                                            popup_btn = True
                                            break
                                    if counter_after_btn_choose > 3:
                                        raise ValueError
                            if popup_btn:
                                break

                        await edit_invoice_page.select('#invoice_custom_field_3', doc_type)
                        time.sleep(1.5)                        
                        await edit_invoice_page.click('#update_invoice')
                        await edit_invoice_page.waitForSelector('#approver')
                        find_continue_button = []
                        while len(find_continue_button) < 3:
                            text = await edit_invoice_page.content()
                            button = BeautifulSoup(text, 'html.parser')
                            find_continue_button = button.find_all(class_='ui-button-text')
                        time.sleep(1)
                        await edit_invoice_page.click('body > div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-draggable.ui-resizable.ui-dialog-buttons > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1)', {'clickCount': 2})
                        await edit_invoice_page.waitForSelector('#invoice_header_tbody')
                        status = 'Posted'
                    

                    elif 'No Processing Required-' + balance_unit in suppliers_found:
                        non_proc_exceptions = {
                        # 'ERHANLAR ULUSLARARASI NAKLİYAT OTOMOTİV SAN. ve TİC. LTD. ŞTİ.': {
                        #     'TUR-FMS': 'ERHANLAR ULUSLARARASI NAK. OTO-3470-NODEPT-MYB-TUR-FMS',
                        #     'TUR-FLT': 'ERHANLAR ULUSLARARASI NAK. OTO-1460091-NODEPT-MYB-TUR-FLT',
                        #     'TUR-PCSD': 'ERHANLAR ULUSLARARASI NAK. OTO-802366-NODEPT-MYB-TUR-PCSD'},
                            'ZERDAL GIDA SAN. VE TİC.LTD.ŞTİ.': {
                                'TUR-FLT': 'ZERDAL GIDA SANAYI VE TIC. LTD-3125377-NODEPT-MYB-TUR-FLT',
                                'TUR-FMS': 'ZERDAL GIDA SANAYI VE TIC. LTD-3125378-NODEPT-MYB-TUR-FMS',
                                'TUR-PCSD': 'ZERDAL GIDA SANAYI VE TIC. LTD-3125379-NODEPT-MYB-TUR-PCSD'
                            },
                            'ARTAS INSAAT SANAYI VE TICARET A.S.': {
                            'TUR-FLT': 'ARTAS INSAAT SANAYI VE TICARET-1495366-NODEPT-MYB-TUR-FLT',
                            'TUR-FMS': 'No Processing Required-' + balance_unit,
                            'TUR-PCSD': 'No Processing Required-' + balance_unit
                            },
                            'GEBİZLİ MİMARLIK DEKORASYON İÇECEK PAZARLAMA LTD.ŞTİ 2020': {
                            'TUR-PCSD': 'GEBIZLI MIMARLIK DEK. I. P. L.-4707379-NODEPT-MYB-TUR-PCSD',
                            'TUR-FLT': 'No Processing Required-' + balance_unit,
                            'TUR-FMS': 'No Processing Required-' + balance_unit
                            }

                            }
                            # 'KENAN ALKAN': {
                            # 'TUR-FMS': 'KENAN ALKAN-2716381-NODEPT-ORA-TUR-FMS',
                            # 'TUR-FLT': 'KENAN ALKAN-2716380-NODEPT-ORA-TUR-FLT',
                            # 'TUR-PCSD': 'KENAN ALKAN-2716382-NODEPT-ORA-TUR-PCSD'}}
                        billing_type = 'NOWF-NoWorkflowNeeded'
                        if supplier_name in non_proc_exceptions.keys():
                            await edit_invoice_page.type('#invoice_supplier_search', non_proc_exceptions[supplier_name][balance_unit])
                        else:
                            await edit_invoice_page.type('#invoice_supplier_search', 'No Processing Required-' + balance_unit)
                        time.sleep(1)
                        await edit_invoice_page.keyboard.press('ArrowDown')
                        await edit_invoice_page.keyboard.press('Enter')

                        await edit_invoice_page.waitForSelector('#invoice_custom_field_6_id_chosen > a > span > ul')
                        await edit_invoice_page.click('#invoice_custom_field_6_id_chosen > a > span > ul')
                        await edit_invoice_page.type('.search-field > input:nth-child(1)', 'VD')
                        time.sleep(2)
                        await edit_invoice_page.keyboard.press('Enter')
                        await edit_invoice_page.type('.search-field > input:nth-child(1)', 'VD04')
                        time.sleep(2)
                        await edit_invoice_page.keyboard.press('Enter')

                        counter = 0
                        while True:
                            await edit_invoice_page.click(f'#invoice_invoice_lines_attributes_{line_number}_account', {'clickCount': 4})
                            await edit_invoice_page.type(f'#invoice_invoice_lines_attributes_{line_number}_account', billing_type)
                            time.sleep(1.5)
                            await edit_invoice_page.keyboard.press('ArrowDown')
                            await edit_invoice_page.keyboard.press('Enter')
                            page_text = await edit_invoice_page.content()
                            soup = BeautifulSoup(page_text, 'html.parser')
                            get_billing_type = soup.find(id=f'invoice_invoice_lines_attributes_{line_number}_account')
                            counter += 1
                            if billing_type == get_billing_type.get_text():                        
                                break
                            popup_btn = False
                            if counter == 2:
                                await edit_invoice_page.click(f'#invoice_invoice_lines_attributes_{line_number}_account_account_picker_popup_button')
                                time.sleep(0.5)
                                await edit_invoice_page.waitForSelector('#account_segment_1_lv_id')
                                time.sleep(0.5)
                                if billing_type != 'NOWF-NoWorkflowNeeded':
                                    await edit_invoice_page.click('#account_segment_1_lv_id_chosen')
                                    time.sleep(0.5)
                                    await edit_invoice_page.keyboard.press('ArrowUp')
                                    time.sleep(0.5)
                                    await edit_invoice_page.keyboard.press('Enter')
                                time.sleep(1)
                                await edit_invoice_page.waitForSelector(f'#invoice_invoice_lines_attributes_{line_number}_account_picker_table_wrapper > div.spiffyTable.dataTable > div.head.picker_search.dynamic-picker > div.page_buttons_right > a')
                                await edit_invoice_page.click(f'#invoice_invoice_lines_attributes_{line_number}_account_picker_table_wrapper > div.spiffyTable.dataTable > div.head.picker_search.dynamic-picker > div.page_buttons_right > a')
                                time.sleep(2)
                                picker_window = 0
                                while True:
                                    page_text = await edit_invoice_page.content()
                                    soup = BeautifulSoup(page_text, 'html.parser')
                                    picker_window += 1
                                    if soup.find(id=f'invoice_invoice_lines_attributes_{line_number}_account_picker_table_wrapper') and picker_window < 3:
                                        time.sleep(2)
                                        print('windows is open')
                                    else:
                                        time.sleep(2)
                                        break
                                await edit_invoice_page.waitForSelector(f'#invoice_invoice_lines_attributes_{line_number}_account > span > span')
                                counter_after_btn_choose = 0
                                while True:
                                    page_text = await edit_invoice_page.content()
                                    soup = BeautifulSoup(page_text, 'html.parser')
                                    # get_billing_type = soup.find(id=f'invoice_invoice_lines_attributes_{line_number}_account')
                                    get_billing_type = soup.find('span', class_='hover_target billingHoverSpec')
                                    print(get_billing_type)
                                    # invoice_invoice_lines_attributes_1325737_account > span > span
                                    counter_after_btn_choose += 1
                                    # print('get_billing_type', get_billing_type.get_text())
                                    print(billing_type)
                                    if get_billing_type:
                                        print('here')
                                        if billing_type == get_billing_type.get_text():
                                            popup_btn = True
                                            break
                                    if counter_after_btn_choose > 3:
                                        raise ValueError
                            if popup_btn:
                                break

                        await edit_invoice_page.click('#update_invoice')
                        find_continue_button = []
                        print('зашел')
                        print(len(find_continue_button))
                        await edit_invoice_page.waitForSelector('#approver')
                        while len(find_continue_button) < 3:
                            text = await edit_invoice_page.content()
                            button = BeautifulSoup(text, 'html.parser')
                            find_continue_button = button.find_all(class_='ui-button-text')
                            print(len(find_continue_button))
                        
                        time.sleep(3)
                        print('вышел из файла')
                        await edit_invoice_page.click('body > div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-draggable.ui-resizable.ui-dialog-buttons > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(2)')
                        print('на кнопку нажал')
                        await edit_invoice_page.waitForSelector('#invoice_header_tbody')
                        print('дождался')                       
                        status = 'Voided'

                    if len(suppliers_found) != 1:
                        await edit_invoice_page.click('.s-saveInvoice')
                        await edit_invoice_page.waitForSelector('#invoice_header_tbody')
                        status = 'Saved'
                except Exception as e:
                    print(e)
                    await edit_invoice_page.bringToFront()
                    await edit_invoice_page.click('.s-saveInvoice')
                    await edit_invoice_page.waitForSelector('#invoice_header_tbody')
                    status = 'Error'
                finally:
                    writer.writerow([invoice_coupa[0], status, suppliers_found, invoice_eportal])
                    f.close()
                    print('****************************************************')
                    break
    await page_void.close()
    await find_supplier.close()
    await supplier_page.close()
    await edit_invoice_page.close()
    await browser.close()

