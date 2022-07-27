from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome(ChromeDriverManager().install())

url = "https://youtube.com"
browser.get(url)

delay = 3

# 검색어 입력
search_name = "playlist"
search_bar = browser.find_element(By.NAME, "search_query")
search_bar.send_keys(search_name)
search_bar.send_keys(Keys.ENTER)
time.sleep(delay)

# Video들이 해당되는 요소 가져오기
videos = browser.find_elements(By.TAG_NAME, 'ytd-video-renderer')

for index, video in enumerate(videos):
  video.screenshot(f"screenshots/{search_name}_{index}.png")

