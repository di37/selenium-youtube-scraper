import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  driver.get(YOUTUBE_TRENDING_URL)
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos

def parse_video(video):
  # title, url, thumbnail_url, channel, views, uploaded,
  # description
  title_tag = video.find_element(By.ID, 'video-title')
  
  title = title_tag.text
  
  URL = title_tag.get_attribute('href')
  
  thumbnail_url_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_url_tag.get_attribute('src')

  metablock = video.find_element(By.CLASS_NAME, 'ytd-video-meta-block').text.split('\n')

  channel_name = metablock[0]

  views = metablock[1]

  uploaded = metablock[2]

  description = video.find_element(By.ID, 'description-text').text

  return {
    'Title': title,
    'Url': URL,
    'Thumbnail_url': thumbnail_url,
    'Channel_name': channel_name,
    'Views': views,
    'Uploaded': uploaded,
    'Description': description
  }

if __name__ == '__main__':
  print('Creating driver')
  driver = get_driver()

  print('Fetching trending videos')
  videos = get_videos(driver)

  print(f'Found {len(videos)} videos.')

  print('Parsing top 10 videos')
  videos_data = [parse_video(video) for video in videos[:10]]
  
  print('Save the data to csv')
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  videos_df.to_csv('trending.csv', index=None)
