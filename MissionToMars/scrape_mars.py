from bs4 import BeautifulSoup
import os
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd
import time
from flask import Flask

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)  

# --------------------------------------------------------- SCRAPE ONCE --------------------------------------------------------

def scrape():
    browser = init_browser()
    mars_collection = {}
    # --------------------------------------------------------- MARS NEWS ---------------------------------------------------------
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)
    html=browser.html
    response = requests.get(url_news)
    soup_news = BeautifulSoup(response.text, 'html.parser')
    
    mars_collection["news_title"] = soup_news.find('div', class_='content_title').text.strip()
    mars_collection["news_para"] = soup_news.find('div', class_='rollover_description_inner').text.strip()
    
    # --------------------------------------------------------- MARS IMAGES ---------------------------------------------------------
    url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_img)
    browser.click_link_by_id('full_image')
    time.sleep(2)
    html = browser.html
    soup_img = BeautifulSoup(html, "html.parser")
    image_url = soup_img.find('img', class_='fancybox-image')['src']
    featured_image_url = "https://www.jpl.nasa.gov" + image_url

    mars_collection["featured_img_url"] = featured_image_url
    
    # --------------------------------------------------------- MARS WEATHER ---------------------------------------------------------
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url_weather)
    soup_weather = BeautifulSoup(response.text, 'html.parser')
    mars_weather = soup_weather.find('div', class_='js-tweet-text-container')
    
    mars_collection["mars_weather"] = mars_weather.text.strip()
    
    # --------------------------------------------------------- MARS FACTS ---------------------------------------------------------
    url_facts = 'https://space-facts.com/mars/'
    mars_tables = pd.read_html(url_facts)
    df = mars_tables[0]
    df.columns = ['MARS PLANET PROFILE', 'FACTS']
    html_fact1 = df.to_html()
    html_fact2 = html_fact1.replace('\n', '')
    
    mars_collection["fact_table"] = html_fact2
    
    # --------------------------------------------------------- MARS HEMISPHERES ----------------------------------------------------
    url_hemi1 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    response = requests.get(url_hemi1)  
    soup_hemi1 = BeautifulSoup(response.text, 'html.parser')
    img_hemi1 = soup_hemi1.find('img', class_='wide-image')['src']
    hemi1_title = soup_hemi1.find('h2', class_='title')
    
    url_hemi2 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    response = requests.get(url_hemi2)
    soup_hemi2 = BeautifulSoup(response.text, 'html.parser')
    img_hemi2 = soup_hemi2.find('img', class_='wide-image')['src']
    hemi2_title = soup_hemi2.find('h2', class_='title')    
    
    url_hemi3 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    response = requests.get(url_hemi3)
    soup_hemi3 = BeautifulSoup(response.text, 'html.parser')
    img_hemi3 = soup_hemi3.find('img', class_='wide-image')['src']
    hemi3_title = soup_hemi3.find('h2', class_='title')
    
    url_hemi4 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    response = requests.get(url_hemi4)
    soup_hemi4 = BeautifulSoup(response.text, 'html.parser')
    img_hemi4 = soup_hemi4.find('img', class_='wide-image')['src']
    hemi4_title = soup_hemi4.find('h2', class_='title')
    
    mars_collection["cereberus_img"] = img_hemi1
    mars_collection["cereberus_title"] = hemi1_title.text.strip()
    mars_collection["schiaparelli_img"] = img_hemi2
    mars_collection["schiaparelli_title"] = hemi2_title.text.strip()
    mars_collection["syrtis_major_img"] = img_hemi3
    mars_collection["syrtis_major_title"] = hemi3_title.text.strip()
    mars_collection["valles_marineris_img"] = img_hemi4
    mars_collection["valles_marineris_title"] = hemi4_title.text.strip()   
    
    mars_collection
    return mars_collection

# >>>   E N D   ...
