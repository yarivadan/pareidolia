from selenium import webdriver
import pandas as pd
import urllib.request as urllib2
import sys
import requests
import io
from PIL import Image
#import getopt
import os
from selenium import webdriver

out_dir = "./images"

def loadCSV():
	url = 'https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv'
	df = pd.read_csv(url, index_col=0)
	return df

def getChromeDriver(chromedriver_path):
	options = webdriver.ChromeOptions()
	options.add_argument('--no-sandbox')
	options.add_argument("--headless")

	driver = webdriver.Chrome(chromedriver_path, chrome_options=options) 
	return driver


df = loadCSV()
driver = getChromeDriver('./chromedriver')

publicd_paintinings = df[(df['Object Name']=='Painting') & (df['Is Public Domain']==True)]
portraits = publicd_paintinings[(publicd_paintinings['Title'].str.contains("Portrait")==True) | (publicd_paintinings['Tags'].str.contains("Portrait")==True)]

for links in portraits['Link Resource']:
  #print(links)

  try:
      driver.get(links)
      html = driver.page_source
  except (urllib2.URLError) as e:
      print(f"ERROR - Could not open link {links} - {e}")
      continue

  offset = html.find("artwork__interaction artwork__interaction--download")

  #print("offset: ", offset)
  if (offset == -1):
      continue
  offset = html[offset:].find('http') + offset
  end = html[offset:].find('.jpg') + offset + 4

  if (end - offset > 300):
      print("URL too long")
      continue

  image_link = html[offset:end]
  #print("image_link: ", image_link)

  image_name = image_link.split('/')[-1]

  image_path = os.path.join(out_dir, image_name)

  if (os.path.exists(image_path)):
  	print("Image already exists: ", image_path)
  	continue

  try:
    image_content = requests.get(image_link).content

  except Exception as e:
    print(f"ERROR - Could not download {image_link} - {e}")

  try:
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert('RGB')

    file_path = image_path
    with open(file_path, 'wb') as f:
      image.save(f, "JPEG", quality=85)
      print(f"SUCCESS - saved {image_link} - as {file_path}")
  except Exception as e:
    print(f"ERROR - Could not save {image_link} - {e}")



