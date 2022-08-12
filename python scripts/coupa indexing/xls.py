import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'Lib', 'xlrd'))
import xlrd
import datetime
exceptions_xls = os.path.join(os.getcwd(), 'required_xls', 'exceptions.xlsx')

def list_of_invoices_eportal(xls_download_folder):
	e_poral_xls_data = []
	for file in os.listdir(xls_download_folder):
	    if file.endswith('.xlsx') and 'InvoiceGrid' in file:
	        print(os.path.join(xls_download_folder, file))
	        wb = xlrd.open_workbook(os.path.join(xls_download_folder, file))
	        sheet = wb.sheet_by_index(0)
	        print(os.path.join(xls_download_folder, file))
	        for i in range(sheet.nrows)[1:-1]:
	        	xlx_row = []	        	
		        xlx_row.append(str(sheet.cell_value(i, 0)))
		        xlx_row.append(str(sheet.cell_value(i, 1)))
		        xlx_row.append(str(sheet.cell_value(i, 2)))
		        xlx_row.append(str(sheet.cell_value(i, 3)))
		        xlx_row.append(str(sheet.cell_value(i, 4)))
		        xlx_row.append(str(sheet.cell_value(i, 8)))
		        day, month, year, hour, minute, second = xlrd.xldate_as_tuple(float(sheet.cell_value(i, 10)), wb.datemode)
		        py_date = datetime.datetime(day, month, year, hour, minute, second)
		        xlx_row.append(datetime.datetime.strptime(str(py_date)[:10], '%Y-%m-%d').strftime('%d/%m/%y'))
		        xlx_row.append(str(sheet.cell_value(i, 25)))
		        e_poral_xls_data.append(xlx_row)
	return e_poral_xls_data

def get_exceptions_coupa():
	exceptions_coupa_vs_eportal = {}
	exceptions_voiding = []
	wb = xlrd.open_workbook(exceptions_xls)
	sheet = wb.sheet_by_index(1)
	for i in range(sheet.nrows)[1:]:
		exceptions_coupa_vs_eportal[str(sheet.cell_value(i, 1)).upper()] = str(sheet.cell_value(i, 0)).upper()
	sheet = wb.sheet_by_index(0)
	exceptions_voiding = [str(i).upper() for i in sheet.col_values(colx=0)[1:]]
	return exceptions_coupa_vs_eportal, exceptions_voiding

