import os
from os import path, mkdir
from datetime import datetime
import sys
import glob
import win32com.client as win32
import logging
import shutil


def get_config_values(config_path):
    with open(config_path) as f:
        lines = f.readlines()
    config_values = {}
    for txt_line in lines:
        tmp_val = txt_line.split("|")
        config_values[tmp_val[0]] = tmp_val[1].replace("\n", "")
    f.close()
    return config_values


def mcopy_file(source_file, destination_path):
    #extract subfolders and recreate on dest path
    path_parts = source_file.split("\\")
    cc_path = path.join(destination_path, path_parts[-3])
    disp_path = path.join(cc_path, path_parts[-2])
    status = ""
    try:
        mkdir(cc_path)
    except Exception as e:
        pass
    try:
        mkdir(disp_path)
    except Exception as e:
        pass
    try:
        dest_path = path.join(disp_path, path_parts[-1])
        if not os.path.exists(dest_path):
            shutil.move(source_file, dest_path)
            status = "success"
        else:
            raise Exception("File already exists at " + dest_path)
    except Exception as e:
        status = str(e)
    return status


def save_report_log(report_name, report_path, report_list):
    if len(report_list) > 0:
        tmp_fname = datetime.now().strftime(report_name+ '_%d%m%Y_%H%M%S.txt')
        tmp_path = path.join(report_path, tmp_fname)
        with open(tmp_path, 'w') as f:
            for line in report_list:
                f.write(f"{line}\n")


def main():
    if getattr(sys, 'frozen', False):
        app_path = path.dirname(sys.executable)
    else:
        app_path = path.dirname(path.abspath(__file__))
    config_path = path.join(app_path, "config.txt")
    config_dict = get_config_values(config_path)

    log_fname = datetime.now().strftime('logfile_%d%m%Y_%H%M%S.log')
    log_path = path.join(app_path, log_fname)
    logging.basicConfig(filename=log_path, level=logging.DEBUG, format="%(asctime)s:%(message)s")
    logging.info("Script started")

    xlsb_files = glob.glob(config_dict["main_path"] + "\\*\\*\\*.xlsb")
    xlsm_files = glob.glob(config_dict["main_path"] + "\\*\\*\\*.xlsm")
    logging.info("XLSB files found:" + str(len(xlsb_files)))
    logging.info("XLSM files found:" + str(len(xlsm_files)))
    files_to_convert = xlsb_files + xlsm_files

    logging.info("Creating Excel Application")
    excel_app = win32.gencache.EnsureDispatch('Excel.Application')
    success_list = []
    errors_list = []
    for exc_file in files_to_convert:
        logging.info("Opening excel file: " + exc_file)
        open_status = False
        try:
            wb = excel_app.Workbooks.Open(exc_file, UpdateLinks=0, IgnoreReadOnlyRecommended=True, Notify=False, CorruptLoad=0)
            open_status = True
        except Exception as e:
            logging.info("Normal workbooks open failed, trying corruptload. Error:" + str(e))
            try:
                wb = excel_app.Workbooks.Open(exc_file, UpdateLinks=0, IgnoreReadOnlyRecommended=True, Notify=False,
                                              CorruptLoad=2)
                open_status = True
            except Exception as e:
                logging.info("Corrupt Load failed. Moving file to errors. Error:" + str(e))
                ret_status = mcopy_file(exc_file, config_dict["errors_path"])
                logging.info("File move status:" + ret_status)
                errors_list.append(exc_file + ";" + str(e) + ", move to errors:" + ret_status)
        if open_status is True:
            new_fname = exc_file[:exc_file.rfind(".", 0, len(exc_file))] + ".xls"
            logging.info("Workbook opened. Saving file to:" + new_fname)
            excel_app.DisplayAlerts = False
            wb.DoNotPromptForConvert = True
            wb.CheckCompatibility = False
            try:
                if not os.path.exists(new_fname):
                    wb.SaveAs(new_fname, FileFormat=56)
                    wb.Close(False)
                    success_list.append(exc_file)
                    ret_status = mcopy_file(exc_file, config_dict["backup_path"])
                    logging.info("Moving file to backup:" + ret_status)
                else:
                    raise Exception("File already exists at " + new_fname)
            except Exception as e:
                wb.Close(False)
                logging.info("File couldn't be saved. Error:" + str(e))
                ret_status = mcopy_file(exc_file, config_dict["errors_path"])
                logging.info("Moving file to errors:" + ret_status)
                errors_list.append(exc_file + ";" + str(e) + ", move to errors:" + ret_status)

    success_list.append("Files converted: " + str(len(success_list)) + " , Files total: " + str(len(files_to_convert)))
    save_report_log("converted", config_dict["report_path"], success_list)
    save_report_log("errors", config_dict["report_path"], errors_list)

    excel_app.Application.Quit()
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


if __name__ == "__main__":
    main()
