from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import openpyxl
import sys, os

def main():
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    else:
        app_path = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(app_path, "chromedriver.exe")
    #driver = webdriver.Chrome("C:\\Users\\pl77906\\PycharmProjects\\python_git\\chromedriver.exe")
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("https://www.behindthename.com/random/")

    gen_story_checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "showextra"))
        )
    gen_story_checkbox.click()
    gen_name_button = driver.find_element(By.CSS_SELECTOR, ".largebutton")
    gen_name_button.click()
    full_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".random-results"))
        )
    name_txt = full_name.text
    driver.close()

    wb = openpyxl.Workbook()
    wb.worksheets[0].cell(1, 1).value = name_txt
    excel_fname = os.path.join(app_path, "test_excel.xlsx")
    print(excel_fname)
    wb.save(excel_fname)
    wb.close()

if __name__ == "__main__":
    main()