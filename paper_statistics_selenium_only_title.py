# !apt-get update
# !pip install selenium
# !apt install chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import time
 
# Crawl the meta data from CVPR Open Access
# Set up a browser to crawl from dynamic web pages 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

urls = ["https://openaccess.thecvf.com/CVPR2022?day=all",
        'https://openaccess.thecvf.com/CVPR2021?day=all',
        'https://openaccess.thecvf.com/CVPR2020?day=2020-06-16']
year = 2022
conference = "cvpr"
file_name = conference + '_' + str(year) + '.csv'
root = r'D:\miniconda\Lib\site-packages\chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
serv = Service(root)
wd = webdriver.Chrome(service=serv,options=chrome_options)

title_total = []
year_total = []
conference_total = []
# Load URL for all CVPR accepted papers.
for url in urls:
    wd.get(url) #FIXME 

    meta_list = [] 
    wait_time = 1
    max_try = 1000


    titles = wd.find_elements(By.CLASS_NAME,"ptitle")
    for title in titles:
        title_total.append(title.text)
        
        

print("The number of total accepted paper titles : ", len(title))

lens = len(titles)
year_arr = [year for i in range(lens)]
conference_arr = [conference for i in range(lens)]
data = {
    'Title': titles,
    'Year': year_arr,
    'Conference': conference_arr,
}
df = pd.DataFrame(data)
df.to_csv(file_name,sep=',',index=False,header=True)