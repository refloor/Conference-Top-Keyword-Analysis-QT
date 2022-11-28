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
        'https://openaccess.thecvf.com/CVPR2020?day=2020-06-16',
        'https://openaccess.thecvf.com/CVPR2020?day=2020-06-17',
        'https://openaccess.thecvf.com/CVPR2020?day=2020-06-18',
        'https://openaccess.thecvf.com/CVPR2019?day=2019-06-18',
        'https://openaccess.thecvf.com/CVPR2019?day=2019-06-19',
        'https://openaccess.thecvf.com/CVPR2019?day=2019-06-20',
        'https://openaccess.thecvf.com/CVPR2018?day=2018-06-19',
        'https://openaccess.thecvf.com/CVPR2018?day=2018-06-20',
        'https://openaccess.thecvf.com/CVPR2018?day=2018-06-21',
        'https://openaccess.thecvf.com/CVPR2017',
        'https://openaccess.thecvf.com/CVPR2016',
        'https://openaccess.thecvf.com/CVPR2015',
        'https://openaccess.thecvf.com/CVPR2014',
        'https://openaccess.thecvf.com/CVPR2013',

        'https://openaccess.thecvf.com/WACV2022',
        'https://openaccess.thecvf.com/WACV2021',
        'https://openaccess.thecvf.com/WACV2020',

        'https://openaccess.thecvf.com/ICCV2021?day=all',
        'https://openaccess.thecvf.com/ICCV2019?day=2019-10-29',
        'https://openaccess.thecvf.com/ICCV2019?day=2019-10-30',
        'https://openaccess.thecvf.com/ICCV2019?day=2019-10-31',
        'https://openaccess.thecvf.com/ICCV2019?day=2019-11-01',
        'https://openaccess.thecvf.com/ICCV2017',
        'https://openaccess.thecvf.com/ICCV2015',
        'https://openaccess.thecvf.com/ICCV2013'
        ]

file_name = 'conference.csv'
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
        title_name = title.text
        conference = url[30:34]
        year = url[34:38]

        title_total.append(title_name)
        conference_total.append(conference)
        year_total.append(year)
    print("The number of total accepted paper titles : ", len(title_total))

data = {
    'Title': title_total,
    'Year': year_total,
    'Conference': conference_total,
}
df = pd.DataFrame(data)
df.to_csv(file_name,sep=',',index=False,header=True)