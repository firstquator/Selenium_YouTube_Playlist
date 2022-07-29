
# Selenium
from sre_constants import MAXREPEAT
from urllib import response
from bs4 import BeautifulSoup
from requests import request
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# YOUTUBE API
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import time

'''

YouTube 데이터를 가져오고는 함수들

'''


YOUTUBE_URL = "https://www.youtube.com"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_KEY = ''  # YOUTUBE API KEY
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = YOUTUBE_API_KEY)

class YoutubeURL:
  BASE = "https://www.youtube.com"
  VIDEO = BASE + "/watch?v="
  EMBED = BASE + "/embed/"

class ChannelTab:
  HOME = 1
  VIDEO = 2
  PLAYLISTS = 3
  COMMUNITY = 4
  CHANNEL = 5
  ABOUT = 6

'''

=========================== YOUTUBE API 기반 Data 가져오기 ===========================

'''


'''

get_channel_id(youtube, query)

description : 검색한 Channel의 channel_id를 가져오는 함수 
@params             youtube : youtube_api build
@params(String)     query   : 채널 이름

return (String)

'''
def get_channel_id(youtube, query):
  try:
    response = youtube.search().list(
      part = "id, snippet",
      q = query,
      maxResults = 1
    ).execute()

    channel_id = response['items'][0]['snippet']['channelId']

  except Exception as e:
    pass
  
  return channel_id

'''

get_video_data(youtube, video_id)

description : Video 정보 가져오기 
@params             youtube : youtube_api build
@params(String)     video_id : video의 ID 값

return (dict)

'''
def get_video_data(youtube, video_id):
  try:
    response = youtube.videos().list(
    part = "snippet, contentDetails, statistics",
    id = video_id,
    ).execute()

    # 해당 video url을 추가해줍니다.
    response['items'][0]['snippet']['video_url'] = YoutubeURL.VIDEO + video_id
  
  except Exception as e:
    pass

  return response


'''

get_channel_videos_data(youtube, channel_id)

description : Channel 동영상 목록 정보 가져오기
@params             youtube : youtube_api build
@params (String)    channel_id : channel의 ID 값

return (dict)

'''
def get_channel_videos_data(youtube, channel_id):
  try:
    channels_response = youtube.channels().list(
    part = "contentDetails",
    id = channel_id,
    ).execute()

    playlist_id = channels_response['items'][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    playlistItems_request = youtube.playlistItems().list(
      part = "snippet, contentDetails",
      playlistId = playlist_id,
      maxResults = 50,
    )

    videos = {
      'items': []
    }
    while playlistItems_request:
      playlistItems_response = playlistItems_request.execute()
      videos['items'] += playlistItems_response['items']

      playlistItems_request = youtube.playlistItems().list_next(
      playlistItems_request, playlistItems_response)
    
  except Exception as e:
    pass

  # 추가 정보 넣기 : 재생시간, 태그, 통계정보(조회수, 좋아요 수 등)
  for video in videos['items']:
    video_info = get_video_data(youtube, video['contentDetails']['videoId'])
    duration = video_info['items'][0]['contentDetails']['duration']

    # tags가 없을 수 있기 때문에 try ~ except 처리를 해준다.
    try:
      tags = video_info['items'][0]['snippet']['tags']
    except Exception as e:
      tags = None
      pass

    statistics = video_info['items'][0]['statistics']
    video_url = video_info['items'][0]['snippet']['video_url']

    video['contentDetails']['duration'] = duration
    video['snippet']['tags'] = tags
    video['statistics'] = statistics
    video['snippet']['video_url'] = video_url
    
  return videos






'''

Selenium 기반 Data Crawling

'''

''' YouTube에서 검색 '''
def search_in_youtube(browser, search):
  youtube_url = 'https://youtube.com'
  browser.implicitly_wait(10)     # 페이지 로딩을 10초 기다리기. 그 전에 로딩이 완료되면 다음 코드를 수행
  browser.get(youtube_url)

  search_bar = browser.find_element(By.NAME, "search_query")
  search_bar.send_keys(search)
  search_bar.send_keys(Keys.ENTER)
  time.sleep(3)

  return browser

''' Channel의 특정 탭 이동 '''
def channel_move(browser, channel_name, tab):
  browser = search_in_youtube(browser, channel_name)
  channel = browser.find_element(By.CLASS_NAME, 'channel-link')
  channel.click()

  video_btn = browser.find_element(By.XPATH, f'//*[@id="tabsContent"]/tp-yt-paper-tab[{tab}]')
  video_btn.click()

  return browser

''' 입력한 횟수만큼 스크롤 '''
def page_scroll(browser, number = 'END'):
  # 스크롤 전 높이
  scroll_location = browser.execute_script("return window.scrollY")

  count = 0
  # 무한 스크롤
  while True:
      # 맨 아래로 스크롤을 내린다.rr2ooo
      time.sleep(2)
      browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

      # 스크롤 사이 페이지 로딩 시간
      time.sleep(1)

      # 스크롤 후 높이
      scroll_height = browser.execute_script("return window.scrollY")
      if scroll_height == scroll_location:
          break
      scroll_location = scroll_height

      # number == END면 끝까지 스크롤
      if number != 'END':
        count += 1
        if count == number:
          break
