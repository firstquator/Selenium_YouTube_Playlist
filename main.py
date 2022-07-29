from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint as pp

import youtube_data as yd

# browser = webdriver.Chrome(ChromeDriverManager().install())
channels = (\
  '구구 Playlist', '쿼츠 Playlist', '찐막 JJINMAK', '민플리PLAYLIST',\
  '미니플리 mini playlist', '세레나Serena', '비쁠', '조거북', '새로플리 ISERO PLAYLIST',\
  '몽땅 M.O.D', '성빈 SUNGBEEN', 'touch playlist : 터치 플레이리스트', '얘들아 사랑해',\
  '나의플레이리스트 NAPLY', '아 퇴사하고 싶다'
)



search_channel = ""
channel_id = yd.get_channel_id(yd.youtube, search_channel)
videos = yd.get_channel_videos_data(yd.youtube, channel_id)
pp(videos['items'])

# 각자 플레이리스트 채널
# vscode 내에 써
# Set -> ()