from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from bs4 import BeautifulSoup

browser = webdriver.Chrome(ChromeDriverManager().install())

url = "https://youtube.com"
browser.get(url)

# 검색어 입력
search_name = "playlist"
search_bar = browser.find_element(By.NAME, "search_query")
search_bar.send_keys(search_name)
search_bar.send_keys(Keys.ENTER)
time.sleep(3)

# Page 스크롤 내리기
body = browser.find_element(By.TAG_NAME, "body")

num_of_pagedowns = 10       # 페이지 다운을 몇 번 할지 정해줍니다.

while num_of_pagedowns:
  body.send_keys(Keys.PAGE_DOWN)    # Selenium이 페이지 다운을 할 수 있도록 코드를 입력
  time.sleep(2)   # 얼마의 시간 뒤에 다시 페이지를 내릴지 시간을 정합니다. 스크롤을 내린 페이지가 로드 될 수 있도록 시간차를 줌.
  num_of_pagedowns -= 1

# Playlist 목록 가져오기 -> 'list'
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
videos = soup.find_all('ytd-video-renderer')
playlists = []

for video in videos:
  video_info = video.find('a', {'id': 'video-title'})
  video_thumbnail = video.find('img', {'id': 'img'})
  playlist_info = {
    'title': video_info.get('title'),                   # 영상 제목
    'views': video_info.get('aria-label').split()[-2],  # 영상 조회수
    'link' : url + video_info.get('href'),              # 영상 link
    'thumbnail': video_thumbnail.get('src'),            # 영상 thumbnail 주소
  }

  playlists.append(playlist_info)

# Display Playlists
count = 1
for playlist in playlists:
  print(f"======================================{count}======================================")
  print(f"title: {playlist['title']}\nviews: {playlist['views']}\nlink: {playlist['link']}\nthumbnail: {playlist['thumbnail']}")
  print("==============================================================================\n")
  count += 1