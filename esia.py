import json
import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def run_driver():
    """ Run webdriver Chrome """
    try:
        current_path = os.getcwd()
        options = Options()
        options.add_experimental_option("prefs", {
            "download.default_directory": current_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True})
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--enable-javascript')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(executable_path=r"D:\Program\Anaconda3\Scripts\chromedriver.exe", chrome_options=options)
        return driver
    except Exception as e:
        print("Error: ", e)

def get_esia_session(login_url: str, personal_page: str, driver) -> bytes or Exception:
    """ Get session in ESIA """
    try:
        driver.get(login_url)
        if requests.get(login_url).status_code == 200:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login'))).send_keys(os.environ['ESIA_LOGIN'])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'password'))).send_keys(os.environ['ESIA_PASSWORD'])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loginByPwdButton'))).click()
            time.sleep(5)
            driver.get(personal_page)
            session = requests.Session()
            r = session.get(personal_page, cookies={c['name']:c['value'] for c in driver.get_cookies()}).text.encode("UTF-8")
            time.sleep(5)
            print("ESIA session: OK!")
            time.sleep(2)
            # Unlock to get document ...
            # print("Get document...")
            # get_doc(driver)
            # time.sleep(10)
            return r
        else:
            print("Error! Status: ", requests.get(login_url).status_code)        
    except Exception as e:
        print(e)
    finally:
        driver.delete_all_cookies()
        driver.close()
        driver.quit()

# Unlock to get document...
# def get_doc(driver):
#     """ Get document: The employment history """
#     try:
#         driver.get("https://www.gosuslugi.ru/600302/1/form")    
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.font-"))).click()
#         time.sleep(10)
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.font-"))).click()
#         time.sleep(30)
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h4.normal.black.text-plain.mb-4.bold"))).click()
#         time.sleep(5)
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.text-plain.gray.small-text.file-name"))).click()
#         time.sleep(10)
#         print("Get document: OK")
#     except Exception as e:
#         print("Error: ", e)

def get_info_from_script(r: bytes):
    """ Get information from JS Object """
    try:
        soup = BeautifulSoup(r, 'html.parser')
        script = soup.find('script')
        if script:
            script_tag_contents = script.string
            with open('source.txt', 'w') as f:
                f.write(script_tag_contents)
            f.close()
        print("Get info: OK!")
        return f
    except Exception as e:
        print("Error in get info: ", e)

def transform_txt_to_json(f):
    """ Transorm JS Object to JSON with the necessary information """
    try:
        f = open('source.txt', 'rt')
        lines = f.readlines()
        f.close()
        with open('source.json', 'w') as json_file:
            line_with_data = lines[2][:-2]
            json_file.write(line_with_data.replace('  data', '{"data"'))
            json_file.write('}')
        json_file.close()
        print("Transform data: OK!")
        return json_file
    except Exception as e:
        print("Error in transform:", e)

def write_info_to_txt(json_file):
    """ Write passport data to .txt file """
    try:
        with open("source.json") as jsonFile:
            json_object = json.load(jsonFile)
            type_docs = json_object["data"]["user"]["person"]["docs"][0]["type"]
            if type_docs != "RF_PASSPORT":
                with open('passport.txt', 'a') as passport_data:
                    passport_data.write(f'Время добавления: {datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M")}\n')
                    passport_data.write(f'ФИО: {json_object["data"]["user"]["formattedName"]}\n')
                    passport_data.write(f'Паспорт РФ: cерия: {json_object["data"]["user"]["person"]["docs"][1]["series"]}, номер: {json_object["data"]["user"]["person"]["docs"][1]["number"]}\n')
                    passport_data.write(f'Выдан: {json_object["data"]["user"]["person"]["docs"][1]["issuedBy"]}\n\n')
            else:    
                with open('passport.txt', 'a') as passport_data:
                    passport_data.write(f'Время добавления: {datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M")}\n')
                    passport_data.write(f'ФИО: {json_object["data"]["user"]["formattedName"]}\n')
                    passport_data.write(f'Паспорт РФ: cерия: {json_object["data"]["user"]["person"]["docs"][0]["series"]}, номер: {json_object["data"]["user"]["person"]["docs"][0]["number"]}\n')
                    passport_data.write(f'Выдан: {json_object["data"]["user"]["person"]["docs"][0]["issuedBy"]}\n\n')
        passport_data.close()
        print("Write info: OK!")
    except Exception as e:
        print("Error in write to file: ", e)

def delete_file():
    """ Delete temp file """
    try:
        os.remove('source.json')
        os.remove('source.txt')
        print("Files was deleted!")
    except OSError as e:
        print("Error: %s" % (e.strerror))

if __name__ == '__main__':
    try:
        runner = run_driver()
        get_session = get_esia_session(login_url='https://esia.gosuslugi.ru/', personal_page='https://lk.gosuslugi.ru/profile/personal', driver=runner)
        if get_session:
            get_info = get_info_from_script(r=get_session)
            transform_data = transform_txt_to_json(f=get_info)
            write_info_to_txt(json_file=transform_data)
            delete_file()
    except Exception as e:
        print("Error: ", e)
