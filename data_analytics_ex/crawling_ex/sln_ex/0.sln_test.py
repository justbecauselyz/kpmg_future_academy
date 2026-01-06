from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 서비스 객체생성
service = Service(ChromeDriverManager().install())
chrome = webdriver.Chrome(service=service)  # page를 가져옴
chrome.get("http://naver.com")

# 5초를 기다림
# time.sleep(10)  # 5 sec

WebDriverWait(chrome, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name-query]"))
)

chrome.close()