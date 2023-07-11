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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


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

# # 4. 팝업 화면 컨트롤
# def change_window(self, target: str):
#     if target == 'parent':
#         # child window close
#         self.driver.close()
#         self.driver.switch_to.window(self.driver.window_handles[0])
#     elif target == 'child':
#         self.driver.switch_to.window(self.driver.window_handles[1])
#     else:
#         print("Wrong target!")


# 현재 열려진 크롬에서 실행하기
openChromeSelenium(False)
# openChromeSelenium(True)

# 다운로드 폴더 설정하는 방법 / 경로를 설정하면 해당 경로에 파일이 다운로드 됨
setDownLoadPath("down_load")

# 자동으로 설치하기
autoInstallerChromeDriver()
logging.info(f"driver_path : {driver_path}")



# 브라우저 실행 및 탭 추가
# browser.execute_script('window.open("about:blank", "_blank");')
# browser.execute_script('window.open("about:blank", "_blank");')
# browser.execute_script('window.open("about:blank", "_blank");')

# tabs = browser.window_handles


# # TAB_1
# browser.switch_to.window(tabs[0])
# browser.get('http://www.naver.com/')

# # 종료하기
# time.sleep(5)

# pyautogui.alert('종료합니다.')
# browser.quit()

driver = webdriver.Chrome(options=chrome_options)

# 웹사이트 접근
driver.get('https://www.kyobo.com/dgt/web/product-official/all-product/search')

# 검색 조건 입력
select_box = Select(driver.find_element(By.ID, 'select-11'))
select_box.select_by_value("99") # 전체

select_box = Select(driver.find_element(By.ID, 'select-12'))
select_box.select_by_value("99") # 전체

select_box = Select(driver.find_element(By.ID, 'select-quan'))
select_box.select_by_visible_text("100개씩 보기")
select_box.select_by_value("100")  

search_button = driver.find_element(By.ID,'searchBtn')  # 검색 버튼의 id 속성에 맞게 수정하세요.
search_button.send_keys(Keys.ENTER)

time.sleep(1.5)

# 'insuList'라는 id를 가진 tbody 요소 찾기
tbody = driver.find_element(By.ID, 'insuList')

# tbody 내의 모든 tr 요소 찾기
tr = tbody.find_elements(By.TAG_NAME, 'tr')

# 정규 표현식으로 패턴 찾기
pattern = r'1000\d{3}'

# 각 행에 대해 반복

count = 1
for row in tr:
    count += 1
    # 각 행의 모든 td 요소 찾기
    td = row.find_elements(By.TAG_NAME, 'td')
    # 각 셀에 대해 반복
    for idx, cell in enumerate(td):
        if idx !=0 and idx%3 == 0:
            # 셀의 텍스트 출력
            print(cell.text)
            print(cell.get_attribute('innerHTML'))

            match = re.search(pattern, cell.get_attribute('innerHTML'))
            if match:
                print(match.group())  # '1000234'
            else:
                print("No match found")
            
            download_button = cell.find_element(By.TAG_NAME,'button')
            download_button.send_keys(Keys.ENTER) 
            # 모든 창의 핸들을 가져옴
            window_handles = driver.window_handles

            # 새로 열린 창(팝업)으로 제어 이동
            driver.switch_to.window(window_handles[-1])
            
            child_tbody = driver.find_element(By.ID, 'pop-periodDownList')
            child_tr = child_tbody.find_elements(By.TAG_NAME, 'tr')

            for product_history in child_tr:
                print(product_history.text)
                product_history.find_elements(By.TAG_NAME, 'a')            

                #url 인코딩
                #"1267683303497_(무)119생활보험(98.04.01).pdf" 
                #"1267683303497_(%EB%AC%B4)119%EC%83%9D%ED%99%9C%EB%B3%B4%ED%97%98(98.04.01).pdf" 

                # from urllib.parse import quote, unquote

                # s = "1267683303497_(무)119생활보험(98.04.01).pdf"
                # encoded = quote(s)
                # decoded = unquote(encoded)

                # print(f"Original: {s}")
                # print(f"Encoded: {encoded}")
                # print(f"Decoded: {decoded}")


            time.sleep(3)

            # 이제 driver는 새로 열린 창(팝업)을 제어합니다.
            # 원래 창으로 돌아가려면 다음과 같이 할 수 있습니다.
            # driver.switch_to.window(window_handles[0])
            
    if count == 5:
        break

pyautogui.alert('종료합니다.')

# PDF 다운로드 링크 클릭
# download_link = driver.find_element_by_id('download-link')  # 다운로드 링크의 id 속성에 맞게 수정하세요.
# download_link.click()

