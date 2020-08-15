#import dependencies
import pandas as pd
import requests
import pymongo
from splinter import Browser
import datetime
import os
from bs4 import BeautifulSoup as bs
import time
   
def init_browser():   
    #set the chromedriver path
    executable_path = {'executable_path':"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # Create browser object
    browser = init_browser()

    #NASA mars news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html,"html.parser")
    news_title = soup.find('div', class_='content_title').text
    print(news_title)
    news_p=soup.find('div', class_='article_teaser_body').text
    print(news_p)

    #mars space images
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html = browser.html
    soup = bs(html,"html.parser")
    image_name= soup.find('article', class_='carousel_item')['alt'] 
    print(image_name)
    image_url=soup.find(class_ = "carousel_item")['style']
    cleaned_image_url=image_url.split("'")[1]
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url= base_url + cleaned_image_url
    print(featured_image_url)

    #mars weather
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(5)
    html = browser.html
    soup = bs(html,"html.parser")
    mars_weather= soup.find('div',class_="css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l r-1udh08x r-1yt7n81 r-ry3cjt").text
    print(mars_weather)

    #mars facts
    url4 = "https://space-facts.com/mars/"
    browser.visit(url4)
    html = browser.html
    soup = bs(html,"html.parser")
    data = pd.read_html(url4)
    mars_facts_df = data[2]
    mars_facts_df.columns = ['Attribute', 'Value']
    mars_facts_df
    facts_html= mars_facts_df.to_html()


    #mars hemispheres
    # url5= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # browser.visit(url5)
    # time.sleep(10)
    # html = browser.html
    # soup = bs(html,"html.parser")
    # hemispheres = soup.find_all('div', class_='item')

    # hemisphere_image_urls = []
    # base_url = 'https://astrogeology.usgs.gov'

    # for hemisphere in hemispheres:
    
    #     title = hemisphere.find('h3').text
    #     hemi_url=hemisphere.find('img', class_ = "wide-image")
    #     print(hemi_url)
    #     full_url= base_url + hemi_url
    #     hemisphere_image_urls.append({"title" : title, "img_url" : full_url})
    
    # hemisphere_image_urls

    hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(5)
    hemis=['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']
    hemisphere_image_urls=[]
    for x in hemis:
        browser.click_link_by_partial_text(x)
        time.sleep(5)
        html=browser.html
        soup=bs(html, 'lxml')
        img_url=soup.find('img', class_='wide-image')['src']
        title=soup.find('h2', class_='title').text
        img_dict={
            'title':title,
            'img_url':(f'https://astrogeology.usgs.gov{img_url}')
            }
        hemisphere_image_urls.append(img_dict)
        browser.visit(hemi_url)
        time.sleep(5)
    browser.quit()
    print(hemisphere_image_urls)

    #store data into dictionary
    mars_data = {
    "News_Title": news_title,
    "Paragraph_Text": news_p,
    "Most_Recent_Mars_Image": featured_image_url,
    "Mars_Weather": mars_weather,
    "Mars_Facts": facts_html,
    "mars_hemisphere": hemisphere_image_urls
    }

    return mars_data











