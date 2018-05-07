__author__ = 'vitorog'

import datetime
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

PUC_LIBRARY_URL = 'http://biblioteca.pucrs.br/renovacao/'
USER_FIELD_NAME = 'cdMatriculaHtml'
CATEGORY_FIELD_NAME = 'idCategoriaHtml'
TECNOPUC_CATEGORY = 'TECNOPUC'
PASSWORD_FIELD_NAME = 'txSenhaHtml'
RENEW_ALL_FIELD_BTN_ID = 'br_renovar_todos'
STUDENT_CATEGORY_FIELD_VALUE = '42'
TECNOPUC_CATEGORY_FIELD_VALUE = '119'

def main():
    if len(sys.argv) < 3:
        print('Missing id, pass')
        print('Usage: python renew_book.py ID PASS [CATEGORY]')
        print('CATEGORY can be student or tecnopuc')
        sys.exit()

    id = sys.argv[1]
    password = sys.argv[2]
    if len(sys.argv) == 4:
        category = sys.argv[3]
    else:
        # Default category
        category = 'student'

    browser = webdriver.PhantomJS()
    print('Accessing website...')
    browser.get(PUC_LIBRARY_URL)
    print('Done.')
    result = ""
    try:
        print('Searching for USER field...')
        id_field = browser.find_element_by_name(USER_FIELD_NAME)
        print('Done.')
        id_field.send_keys(id)
        browser.implicitly_wait(2)
        print('Searching for CATEGORY field...')
        category_field = Select(WebDriverWait(browser, 2).until(
           EC.presence_of_element_located((By.NAME, CATEGORY_FIELD_NAME))))
        print('Done.')
        print('Selecting right category...')
        if category == 'student':
            category_field.select_by_value(STUDENT_CATEGORY_FIELD_VALUE)
        elif category == 'tecnopuc':
            category_field.select_by_value(TECNOPUC_CATEGORY_FIELD_VALUE)
        else:
            print('Invalid category.')
            return
        print('Searching for PASSWORD field...')
        password_field = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.NAME, PASSWORD_FIELD_NAME)))
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        print('Done.')
        print('Searching for RENEW ALL field...')
        browser.implicitly_wait(2)
        renew_field =  WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, RENEW_ALL_FIELD_BTN_ID)))
        js_confirm = 'window.confirm = function(){return true;}'  # .js function to confirm a popup
        browser.execute_script(js_confirm)
        renew_field.click()
        print('Done.')
        print('Finished successfully.')
        result = 'success'
    except TimeoutException as e:
        print('Process timeout')
        result = 'failed'
    except Exception as e:
        print("Unexpected error:", e)
    finally:
        print('Saving result screenshot...')
        browser.save_screenshot(result + '_' + str(datetime.datetime.now()) + '.png')
        browser.quit()


if __name__ == '__main__':
    main()
