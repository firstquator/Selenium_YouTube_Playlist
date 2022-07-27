from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from bs4 import BeautifulSoup

browser = webdriver.Chrome(ChromeDriverManager().install())

url = "https://youtube.com"
browser.implicitly_wait(10)     # 페이지 로딩을 10초 기다리기. 그 전에 로딩이 완료되면 다음 코드를 수행
browser.get(url)

# 검색어 입력
search_name = "playlist"
search_bar = browser.find_element(By.NAME, "search_query")
search_bar.send_keys(search_name)
search_bar.send_keys(Keys.ENTER)
time.sleep(3)

# Page 스크롤 내리기
'''
body = browser.find_element(By.TAG_NAME, "body")

num_of_pagedowns = 10       # 페이지 다운을 몇 번 할지 정해줍니다.

while num_of_pagedowns:
  body.send_keys(Keys.PAGE_DOWN)    # Selenium이 페이지 다운을 할 수 있도록 코드를 입력
  time.sleep(2)                     # 얼마의 시간 뒤에 다시 페이지를 내릴지 시간을 정합니다. 스크롤을 내린 페이지가 로드 될 수 있도록 시간차를 줌.
  num_of_pagedowns -= 1
'''

# Playlist 제목, 조회수, 링크, 썸네일 가져오기 -> 'list'
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
videos = soup.find_all('ytd-video-renderer')
playlists = []

for video in videos:
  video_info = video.find('a', {'id': 'video-title'})
  video_thumbnail = video.find('img', {'id': 'img'})
  playlist_info = {
    'title': video_info.get('title'),                                                 # 영상 제목
    'views': video_info.get('aria-label').split()[-2],                                # 영상 조회수
    'thumbnail': video_thumbnail.get('src'),                                          # 영상 thumbnail 주소
    'link' : url + video_info.get('href'),                                            # 영상 link
    'video_src': url + '/embed' + '/' + video_info.get('href').lstrip('/watch?v=')    # 영상 소스 코드
  }

  playlists.append(playlist_info)

# Playlist 좋아요, 세부 노래 목록 가져오기
playlist_songs = []
for playlist in playlists:
  browser.implicitly_wait(10)     # 페이지 로딩을 10초 기다리기. 그 전에 로딩이 완료되면 다음 코드를 수행
  browser.get(playlist['link'])
  try:
    browser.find_element(By.CSS_SELECTOR, 'yt-formatted-string.more-button').click()  # 노래 목록 보기 버튼 클릭
  except Exception as e:
    pass

  playlist_html = browser.page_source
  playlist_soup = BeautifulSoup(playlist_html, 'lxml')
  
  like = playlist_soup.find('yt-formatted-string', {'id': 'text'}).text                     # 영상 좋아요 수
  duration = playlist_soup.find('span', {'class': 'ytp-time-duration'}).text                # 영상 재생 길이 -> 광고 뜨는 경우 생각해야함
  if duration == 'LIVE':                                                                    # 영상이 LIVE라면 저장하지 않는다.
    continue

  try:
    songs = playlist_soup.find_all('ytd-compact-video-renderer')                            # Playlist 내 노래 목록들
    for song in songs:
      song_info = {
        'title': song.find('span', {'id': 'video-title'}).get('title'),                     # 노래 제목
        'link': url + song.find('a', {'class': 'ytd-compact-video-renderer'}).get('href')   # 노래 link
      }

      playlist_songs.append(song_info)
  except Exception as e:
    pass



  playlist['like'] = like
  playlist['duration'] = duration
  playlist['playlist_songs'] = playlist_songs

# Display Playlists
count = 1
for playlist in playlists:
  print(f"====================================== {count} ======================================")
  print(f"title: {playlist['title']}\n\
          views: {playlist['views']}\n\
          link: {playlist['link']}\n\
          thumbnail: {playlist['thumbnail']}\n\
          video_src: {playlist['video_src']}\n\
          like: {playlist['like']}\n\
          duration: {playlist['duration']}\n\
          playlist_songs: {playlist['playlist_songs']}\n")
  print("================================================================================\n")
  count += 1
