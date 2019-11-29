# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import pprint
from splinter import Browser
import pandas as pd
import time



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    news_url = "https://mars.nasa.gov/news/"
    fact_url = "https://space-facts.com/mars/"
    pic_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    mars_pic_url = "https://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    


    # Mars hemisphere pics ************************************************
    browser.visit(mars_pic_url)
    html = browser.html
    # Parse HTML for pic titles
    soup = BeautifulSoup(html, 'html.parser')
    h3 = soup.find_all('h3')
    # Collect titles in list.
    pic_names = [name.text for name in h3]
    ref_list = []
    # Search for image href one title at a time.
    for name in pic_names:
        browser.click_link_by_partial_text(name)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        test = soup.find_all('div', class_='wide-image-wrapper')
        for image in test:
            img = "https://web.archive.org/" + image.find_all('img',class_='wide-image')[0]['src']
            ref_list.append(img)
        browser.back()

    hemisphere_image_urls = [{"title" : pic_names[0], "img_url" : ref_list[0]},
                            {"title" : pic_names[1], "img_url" : ref_list[1]},
                            {"title" : pic_names[2],"img_url" : ref_list[2]},
                            {"title" : pic_names[3],"img_url" : ref_list[3]}]

    # Mars fact table ********************************************************
    mars_fact = pd.read_html(fact_url)
    fact_df = pd.DataFrame(mars_fact[0])
    fact_df.rename(columns = {0:'Statistic',1:'Measured'}, inplace = True)
    mars_facts = fact_df.to_html()  # html table

    # Mars weather from Twitter **********************************************
    browser.visit(tweet_url)
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    big_list = []
    twtpage = soup.find('body')
    twt = twtpage.find_all('div',class_='tweet')
    for stuff in twt:
        content = stuff.find_all('div',class_='content')
        big_list.append(content[0].find('p').text)
    mars_weather = big_list[0] # get most recent weather tweet.
    #print(big_list[0])

    # Mars Featured Picture ***************************************************
    browser.visit(pic_url)
    #html = browser.html
    # Parse HTML with Beautiful Soup
    #soup = BeautifulSoup(html, 'html.parser')
    time.sleep(2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    apage = soup.find('body', class_='dark_background')
    img_box = apage.find('div', class_='fancybox-inner')
    target_img = img_box.find('img')
    print(target_img)
    featured_image_url = "https://www.jpl.nasa.gov" + target_img['src'] # image path
    #featured_image_url = "https://www.jpl.nasa.gov" + "/testpath" # image path """

    # Mars headline ************************************************************
    response = requests.get(news_url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
    title_results = soup.find_all('div', class_='content_title') #content_title
    desc_results = soup.find_all('div', class_='rollover_description_inner')
    news_title = title_results[0].text.strip('\n')
    news_p = desc_results[0].text.strip('\n')

    result_dict = {"news_title" : news_title, "news_p" : news_p,"mars_weather" : mars_weather,
    "featured_image_url" : featured_image_url, "mars_facts" : mars_facts, "hemisphere_image_urls" : hemisphere_image_urls}
    return result_dict

   



