__author__ = 'vitorog'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  TimeoutException
import sys
import datetime

PUC_LIBRARY_URL = 'http://www3.pucrs.br/portal/page/portal/biblioteca/Capa/Renovacao'
USER_FIELD_ID = 'uid'
CATEGORY_FIELD_ID = 'idCategoria'
TECNOPUC_CATEGORY = 'Tecnopuc'
PASSWORD_FIELD_NAME = 'txSenha'
RENEW_ALL_FIELD_TEXT = 'Renovar TODOS'

def main():
    if len(sys.argv) < 3:
        print('Missing id and pass')
        print('Usage: python renew_book.py ID PASS')
        sys.exit()

    id = sys.argv[1]
    password = sys.argv[2]

    browser = webdriver.PhantomJS()
    print('Accessing website...')
    browser.get(PUC_LIBRARY_URL)
    print('Done.')
    result = ""
    try:
        print('Searching for USER field...')
        id_field = browser.find_element_by_id(USER_FIELD_ID)
        print('Done.')
        id_field.send_keys(id)
        id_field.send_keys(Keys.RETURN)
        browser.implicitly_wait(2)
        print('Searching for CATEGORY field...')
        category_field = Select(WebDriverWait(browser, 2).until(
           EC.presence_of_element_located((By.NAME, CATEGORY_FIELD_ID))))
        print('Done.')
        print('Selecting right category...')
        for opt in category_field.options:
            if TECNOPUC_CATEGORY in opt.text:
                print('Found category.')
                opt.click()
                break
        print('Searching for PASSWORD field...')
        password_field = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.NAME, PASSWORD_FIELD_NAME)))
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        print('Done.')
        print('Searching for RENEW ALL field...')
        browser.implicitly_wait(2)
        renew_field =  WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.LINK_TEXT, RENEW_ALL_FIELD_TEXT)))
        renew_field.click()
        print('Done.')
        print('Finished successfully.')
        result = 'success'
    except TimeoutException as e:
        print('Process timeout')
        result = 'failed'
    finally:
        print('Saving result screenshot...')
        browser.save_screenshot(result + '_' + str(datetime.datetime.now()) + '.png')
        browser.quit()


if __name__ == '__main__':
    main()

