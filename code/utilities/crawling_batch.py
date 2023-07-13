# pip install selenium 
# pip install BeautifulSoup4
# pip install pyautogui
# pip install chromedriver-autoinstaller
# pip install openpyxl
# 드라이버 자동설치할때 크롬 설치된 위치가 Program Files (x86) 이면,
# chromedriver_autoinstaller\utils.py 수정 필요
import os
import time
import pandas as pd
import numpy as np
import pyautogui
import chromedriver_autoinstaller
import logging
import re
import requests
import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

WORKING_DIR     = os.path.dirname(os.path.abspath(__file__))
CODE_DIR        = os.path.dirname(WORKING_DIR)   
ROOT_DIR        = os.path.dirname(CODE_DIR)
PDF_DIR         = os.path.join(ROOT_DIR,"pdf") 
EXCEL_DIR       = os.path.join(PDF_DIR,"product_list") 
EXCEL_FILE_NM   = "Product_list.xlsx"
MAIN_TR_SIZE    = 0

chrome_options = Options()
# chrome_options.add_argument('headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
# chrome_options.add_argument('--window-size= x, y') #실행되는 브라우저 크기를 지정할 수 있습니다.
chrome_options.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
# chrome_options.add_argument('--start-fullscreen') #브라우저가 풀스크린 모드(F11)로 실행됩니다.
# chrome_options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
# chrome_options.add_argument('--mute-audio') #브라우저에 음소거 옵션을 적용합니다.
# chrome_options.add_argument('incognito') #시크릿 모드의 브라우저가 실행됩니다.

# 1. 현재창에서 셀레니움을 실행 할지 설정
def openChromeSelenium(isopenChromeSelenium=False):
    if isopenChromeSelenium:
        # cmd 창을 실행해서 현재 크롬에서 실행
        pyautogui.hotkey("win", "r")  # 단축키 : win + r 입력
        pyautogui.write('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium_chrome"')  # 프로그램 명 입력
        pyautogui.press("enter")  # 엔터 키 입력

        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 2. 크롬에서 파일 다운로드 경로 설정하기
def setDownLoadPath(download_path=None):
    # download_path = "down_load_path"
    if download_path != None:
        # os.path.abspath("Scripts") : 현재 작업 경로에 Scripts를 더함   =>  "C:\Python35\Scripts" 현재 경로에        download_path = os.path.abspath(download_path)
        prefs = {"download.default_directory": download_path}
        logging.info(download_path)
        chrome_options.add_experimental_option("prefs", prefs)

# 3. 크롬 드라이버 자동으로 설치하게
def autoInstallerChromeDriver():
    global driver_path
    # 크롬을 자동으로 받게 하는 옵션 / 설치되어 있는지 확인
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        logging.info(f"chrom driver is insatlled: {driver_path}")
    else:
        logging.info(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)

# 5. 상품 list excel DataFrame load
def MakeProductListDataFrame():
    df = pd.read_excel(f"{EXCEL_DIR}\{EXCEL_FILE_NM}", sheet_name="Data")
    df = df.astype(str)
    return df

# 6. 보험상품명, 보험상품판매명 get
def getInsuPdtNm(input_df : pd.DataFrame, is_pdt_cd : str, ap_st_dt):    
    df = input_df    
    df = df[['보험상품코드','보험상품명','보험상품판매명','적용시작일자','적용종료일자']].drop_duplicates()
    df = df[df['보험상품코드'].isin([(is_pdt_cd)])]       

    if len(df) != 0:
        df = df[(df['적용시작일자'] <= ap_st_dt) & (df['적용종료일자'] >= ap_st_dt)]        
        if len(df) != 0:
            is_pdt_nm = df['보험상품명'].values[0]
            is_pdt_sale_nm = df['보험상품판매명'].values[0]
            return(is_pdt_nm,is_pdt_sale_nm)
        else:
            return (is_pdt_cd, is_pdt_cd)
    else:
        return (is_pdt_cd,is_pdt_cd)
    
# 7. 
def setSearchCondition(input_driver : webdriver, sale_cd : str, is_dv_cd : str, is_dtl_dv_cd, how_many : str):

    # 판매여부 : 전체(99), 판매중(Y), 판매중지(N)
    select_box = Select(input_driver.find_element(By.ID, 'select-11'))
    select_box.select_by_value(sale_cd)
    
    # 보험종류  
    # 전체(99) , 교육보험(PAMS01), 연금보험(PAMS02), 저축보험(PAMS03), 보장성보험(PAMS04)
    # 기업보험(PAMS05), 통신판매전용상품(PAMS06), 방카슈랑스전용상품(PAMS07)
    # 퇴직연금(PAMS08), 퇴직보험(PAMS09), 온라인보험(PAMS10)
    select_box = Select(input_driver.find_element(By.ID, 'select-12'))
    select_box.select_by_value(is_dv_cd) # 전체

    # 보험세부구분 전체(99)
    select_box = Select(input_driver.find_element(By.ID, 'select-13'))
    select_box.select_by_value(is_dtl_dv_cd) # 전체

    # n개씩 보기
    select_box = Select(input_driver.find_element(By.ID, 'select-quan'))
    select_box.select_by_value(how_many) 
    select_box.select_by_visible_text(f"{how_many}개씩 보기")

    # 조회
    search_button = input_driver.find_element(By.ID,'searchBtn')
    search_button.send_keys(Keys.ENTER)

    return int(how_many)

# ----------------------------------------------------------------------------------------- #
# setting --------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s::%(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

# 현재 열려진 크롬에서 실행하기
openChromeSelenium(False)

# 다운로드 폴더 설정하는 방법 / 경로를 설정하면 해당 경로에 파일이 다운로드 됨
setDownLoadPath("down_load")

# 자동으로 설치하기
autoInstallerChromeDriver()
logging.info(f"driver_path : {driver_path}")

# ----------------------------------------------------------------------------------------- #
# start------------------------------------------------------------------------------------ #
# ----------------------------------------------------------------------------------------- #

# 데이터프레임 load
product_df = MakeProductListDataFrame()
logging.info(f"product_df : {product_df}")

# 크롬드라이버 load
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.kyobo.com/dgt/web/product-official/all-product/search')
driver.implicitly_wait(time_to_wait=10)

# 검색 조건 입력
MAIN_TR_SIZE = setSearchCondition(driver, "Y", "PAMS01", "99", "10") #판매중 교육보험
# MAIN_TR_SIZE = setSearchCondition(driver, "Y", "PAMS03", "99", "10") #판매중 저축보험
#MAIN_TR_SIZE = setSearchCondition(driver, "Y", "99", "99", "10")
#setSearchCondition(driver, "99", "99", "99", "20")
#setSearchCondition(driver, "Y", "PAMS02", "99", "20")

time.sleep(10)

total_count_element = \
    WebDriverWait(driver,10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//*[@id="totalCnt"]')))
total_count = int(total_count_element[0].text)

wait_product_list_table = \
    WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'tblist')))
m_td = driver.find_element(By.CLASS_NAME, 'tblist')

wait_insuList = \
    WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="insuList"]')))
m_insuList = m_td.find_element(By.ID, 'insuList')

wait_tr = \
    WebDriverWait(driver,10).until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

m_tr = m_insuList.find_elements(By.TAG_NAME, 'tr')

max_page = math.ceil(total_count / len(m_tr))

logging.info(f"total_data_row_count     : {total_count}")
logging.info(f"main_tr_size             : {MAIN_TR_SIZE}")
logging.info(f"max_page_num             : {max_page}")

time.sleep(0.5)

current_page = 1
logging.info("start current_page : {current_page}")

for current_data_count in range(1, total_count+1): 

    for m_tr_cnt in range(1, MAIN_TR_SIZE+1):

        m_tr = \
            WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, f'//*[@id="insuList"]/tr[{m_tr_cnt}]')))

        m_td_4 = \
            WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, f'//*[@id="insuList"]/tr[{m_tr_cnt}]/td[4]')))
        
        # logging.info(m_td_4.get_attribute('innerHTML'))

        match = re.search(r'1000\d{3}', m_td_4.get_attribute('innerHTML'))

        if match:
            is_pdt_cd = match.group()
            logging.info(f"first get [is_pdt_cd] : {is_pdt_cd}")        
        else:
            logging.error("No match found")
            continue

        time.sleep(0.2)

        WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'.btn.sm')))
        download_button = m_td_4.find_element(By.CSS_SELECTOR,'.btn.sm')
        download_button.send_keys(Keys.ENTER)

        # --- 팝업 진입 --- #

        child_tbody         = WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="pop-periodDownList"]')))
        child_tr_max_count  = WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="pop-totalCnt"]')))

        logging.info(f"Pop-up [child row total count] : {child_tr_max_count.text}")

        for child_tr_cnt in range(1, int(child_tr_max_count.text)+1):

            child_tr_td_1 = WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, f'//*[@id="pop-periodDownList"]/tr[{child_tr_cnt}]/td[1]')))
            #child_tr_td_2 = WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, f'//*[@id="pop-periodDownList"]/tr[{child_tr_cnt}]/td[2]')))
            child_tr_td_3 = WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, f'//*[@id="pop-periodDownList"]/tr[{child_tr_cnt}]/td[3]')))
            #child_tr_td_4 = WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, f'//*[@id="pop-periodDownList"]/tr[{child_tr_cnt}]/td[4]')))

            history_str     = child_tr_td_1.text.split("~")           # 이력 문자열
            start_date      = history_str[0].strip().replace("-", "") # 이력 시작일자 
            end_date        = history_str[1].strip().replace("-", "") # 이력 종료일자

            if len(end_date) == 0:
                end_date = '99991231'

            # 이력에 따라 판매명 달라질수 있으므로 계속 호출
            pdt_nm      = getInsuPdtNm(product_df, is_pdt_cd, start_date)  

            # pdf를 저장시키는 폴더명에 사용할 상품명
            folder_nm   = f"{is_pdt_cd}_{pdt_nm[0]}"

            # pdf 파일에 사용할 상품 판매명
            pdt_sale_nm = pdt_nm[1]
            
            logging.info(f"start_date : {start_date}")                   
            logging.info(f"end_date : {end_date}")
            logging.info(f"is_pdt_cd : {is_pdt_cd}")
            logging.info(f"folder_nm : {folder_nm}")
            logging.info(f"pdt_sale_nm : {pdt_sale_nm}")
            
            #ico_file_button = child_tr_td_3.find_element(By.TAG_NAME,'a')
            ico_file_button = \
                WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, f'//*[@id="pop-periodDownList"]/tr[{child_tr_cnt}]/td[3]/a')))

            href_value = ico_file_button.get_attribute('href')      

            match = re.search(r'"(.+)"', href_value)
            if match:
                pdf_filename = match.group(1)
                logging.info(f"fing child row pdf file name : {pdf_filename}")
            else:
                logging.error("No match found : file name")
                continue

            # API 호출
            # https://www.kyobo.com/file/ajax/download?fName=/dtc/pdf/mm/파일명
            # 아래 잠시만
            donwload_url = f"https://www.kyobo.com/file/ajax/download?fName=/dtc/pdf/mm/"
            donwload_url = donwload_url + pdf_filename
            response = requests.get(donwload_url)
            
            if not os.path.exists(f"{PDF_DIR}\{folder_nm}"):
                os.makedirs(f"{PDF_DIR}\{folder_nm}")

            # PDF 파일로 저장
            with open(f"{PDF_DIR}\{folder_nm}\{pdt_sale_nm}-{start_date}-{end_date}.pdf", "wb") as f:
                f.write(response.content)

        child_x_button = WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="pop-period-down"]/div/button')))
        child_x_button.send_keys(Keys.ENTER) 

        # --- 팝업 종료 --- #

        time.sleep(0.5) 

        if current_page < max_page and (current_data_count % MAIN_TR_SIZE == 0):
            current_page += 1
            driver.execute_script(f"movePage({str(current_page)})")
            logging.info(f"function called movePage --> {current_page}")   

        logging.info(f"current_page : {current_page}")
        logging.info(f"current_data_count : {current_data_count}")

        if current_data_count == total_count:
            break

# ----------------------------------------------------------------------------------------- #
# end-------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------- #
logging.info("ended .. ")
pyautogui.alert('종료합니다.')