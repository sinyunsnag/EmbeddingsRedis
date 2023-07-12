# pip install selenium 
# pip install BeautifulSoup4
# pip install pyautogui
# pip install chromedriver-autoinstaller
# 드라이버 자동설치할때 크롬 설치된 위치가 Program Files (x86) 이면,
# chromedriver_autoinstaller\utils.py 수정 필요
import os
import time
import pyautogui
import chromedriver_autoinstaller
import logging
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException



MAX_RETRY = 5
retry_count = 0

chrome_options = Options()
chrome_options.add_argument('headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
# chrome_options.add_argument('--window-size= x, y') #실행되는 브라우저 크기를 지정할 수 있습니다.
# chrome_options.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
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
        print(download_path)
        chrome_options.add_experimental_option("prefs", prefs)

# 3. 크롬 드라이버 자동으로 설치하게
def autoInstallerChromeDriver():
    global driver_path
    # 크롬을 자동으로 받게 하는 옵션 / 설치되어 있는지 확인
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver_path = f'./{chrome_ver}/chromedriver.exe'
    if os.path.exists(driver_path):
        print(f"chrom driver is insatlled: {driver_path}")
    else:
        print(f"install the chrome driver(ver: {chrome_ver})")
        chromedriver_autoinstaller.install(True)


# 현재 열려진 크롬에서 실행하기
openChromeSelenium(False)
# openChromeSelenium(True)

# 다운로드 폴더 설정하는 방법 / 경로를 설정하면 해당 경로에 파일이 다운로드 됨
setDownLoadPath("down_load")

# 자동으로 설치하기
autoInstallerChromeDriver()
logging.info(f"driver_path : {driver_path}")

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.kyobo.com/dgt/web/product-official/all-product/search')
driver.implicitly_wait(time_to_wait=10)

# 검색 조건 입력
select_box = Select(driver.find_element(By.ID, 'select-11'))
select_box.select_by_value("99") # 전체

select_box = Select(driver.find_element(By.ID, 'select-12'))
select_box.select_by_value("99") # 전체

select_box = Select(driver.find_element(By.ID, 'select-12'))
select_box.select_by_value("99") # 전체

select_box = Select(driver.find_element(By.ID, 'select-quan'))
select_box.select_by_visible_text("100개씩 보기")
select_box.select_by_value("100")  

search_button = driver.find_element(By.ID,'searchBtn')  # 검색 버튼의 id 속성에 맞게 수정하세요.
search_button.send_keys(Keys.ENTER)


wait_product_list_table = \
    WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'tblist')))
m_td = driver.find_element(By.CLASS_NAME, 'tblist')

wait_insuList = \
    WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="insuList"]')))
m_insuList = m_td.find_element(By.ID, 'insuList')
print(f"m_insuList : {m_insuList}")

wait_tr = \
    WebDriverWait(driver,10).until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
m_tr = m_insuList.find_elements(By.TAG_NAME, 'tr')

time.sleep(0.5)

for row in m_tr:

    time.sleep(0.5)
    print("before get m_dt")
    retry_count = 0
    while retry_count < MAX_RETRY:
        try:
            m_td = row.find_elements(By.TAG_NAME, 'td')
            # 필요한 작업을 수행합니다.
            break
        except StaleElementReferenceException:
            retry_count += 1
            print("for get m_dt --- retry")
            time.sleep(1)  # 잠시 대기
       
    print("after get m_dt")

    for idx, cell in enumerate(m_td):
        if idx == 3:
            # 셀의 텍스트 출력
            # print(cell.text)
            print(cell.get_attribute('innerHTML'))
            pattern = r'1000\d{3}'
            match = re.search(pattern, cell.get_attribute('innerHTML'))
            if match:
                is_pdt_cd = match.group()                
            else:
                print("No match found")
                continue

            time.sleep(0.2)

            WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'.btn.sm')))
            download_button = cell.find_element(By.CSS_SELECTOR,'.btn.sm')
            download_button.send_keys(Keys.ENTER)
            #download_button.click()

            # 모든 창의 핸들을 가져옴
            # window_handles = driver.window_handles

            # 새로 열린 창(팝업)으로 제어 이동
            # driver.switch_to.window(window_handles[-1])
            # //*[@id="pop-period-down"]/div/div[2]/div[3]/table
            retry_count = 0
            while retry_count < MAX_RETRY:
                try:
                    child_tbody = WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="pop-periodDownList"]')))

                    # 필요한 작업을 수행합니다.
                    break
                except StaleElementReferenceException:
                    retry_count += 1
                    print("for get child_tbody --- retry")
                    time.sleep(1)  # 잠시 대기
            
            #child_tbody = WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="pop-periodDownList"]')))
            #child_tbody = driver.find_element(By.ID, 'pop-periodDownList')
            retry_count = 0
            while retry_count < MAX_RETRY:
                try:
                    child_tr = child_tbody.find_elements(By.TAG_NAME, 'tr')
                    # 필요한 작업을 수행합니다.
                    break
                except StaleElementReferenceException:
                    retry_count += 1
                    print("for get child_tr --- retry")
                    time.sleep(1)  # 잠시 대기

            

            for row_history in child_tr:
                retry_count = 0
                while retry_count < MAX_RETRY:
                    try:
                        child_td = row_history.find_elements(By.TAG_NAME, 'td') 

                        # 필요한 작업을 수행합니다.
                        break
                    except StaleElementReferenceException:
                        retry_count += 1
                        print("for get child_td --- retry")
                        time.sleep(1)  # 잠시 대기


                for idx, product_history in  enumerate(child_td):
                    if idx == 0:
                        history_str = product_history.text.split("~")
                        start_date = history_str[0].strip().replace("-", "")
                        end_date = history_str[1].strip().replace("-", "")     
                        print(f"start_date : {start_date}")                   
                        print(f"end_date : {end_date}")
                        print(f"is_pdt_cd : {is_pdt_cd}")

                    if idx == 1:                        
                        ico_file_button = product_history.find_element(By.TAG_NAME,'a')
                        href_value = ico_file_button.get_attribute('href')      
                        # ico_file_button.send_keys(Keys.ENTER)                     
                        match = re.search(r'"(.+)"', href_value)
                        pdf_filename = ""
                        if match:
                            pdf_filename = match.group(1)
                        else:
                            print("No match found : file name")
                            continue

                        # API 호출
                        # https://www.kyobo.com/file/ajax/download?fName=/dtc/pdf/mm/파일명
                        # 아래 잠시만
                        # donwload_url = f"https://www.kyobo.com/file/ajax/download?fName=/dtc/pdf/mm/"
                        # donwload_url = donwload_url + pdf_filename
                        # response = requests.get(donwload_url)
                        
                        # # PDF 파일로 저장
                        # with open(f"{is_pdt_cd}-{start_date}-{end_date}.pdf", "wb") as f:
                        #     f.write(response.content)   

            child_x_button = WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="pop-period-down"]/div/button')))
            # child_x_button = driver.find_element(By.XPATH, '//*[@id="pop-period-down"]/div/button')
            child_x_button.send_keys(Keys.ENTER) 

            time.sleep(0.5)
            
            #driver.switch_to.window(window_handles[0])                
          
    # if count == 3:
    #     break

pyautogui.alert('종료합니다.')