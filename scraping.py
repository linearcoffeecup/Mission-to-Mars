#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)


    news_title, news_paragraph = mars_news(browser)
    hemisphere_list  =  mars_hemispheres(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere": hemisphere_list
        
        }



    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')


    slide_elem.find('div', class_='content_title')

    try:

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
   

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
   

    except AttributeError:
        return None, None

    return  news_title,  news_p



# ### Image scraping below

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():

    try:

        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html()


def mars_hemispheres(browser):

    # Scrape High-Resolution Mars’ Hemisphere Images and Titles

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_dict = {}
    hemi_list = []
    img_h_soup_info_url = []
    img_h_soup_info_name = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    html_h = browser.html
    img_h_soup = soup(html_h, 'html.parser')

    try:
        #Name
        #
        # obtain the name from the image tag
        #this image in on the browser page at browser(url)

        results_name = img_h_soup.find_all('div', class_="item")

        for name in results_name:
            
            alt_name = name.find('img', class_='thumb').get('alt').split()[0]

            #Update the name list

            img_h_soup_info_name.append(alt_name)

        #URL
        #
        #finding the new relative url
        #these links are on the same browser page at browser(url)

        results_div = img_h_soup.find_all('div', class_="item")

        for result in results_div:
            rel_url = result.find('a', class_="itemLink product-item").get('href')

            #adding the new url to the base url

            new_url = f'https://marshemispheres.com/{rel_url}'

            #using browser to go to the rel_url
            #this is "clicking on the url"

            browser.visit(new_url)
            
            # Writing code to retrieve html info on a new browser page.

            html_h = browser.html
            img_h_soup = soup(html_h, 'html.parser')

            #this image (.jpg) is on the browser page browser(new_url)
            #find the .jpg by finding the img tag
            
            img_jpg = img_h_soup.find('img', class_ = "wide-image")
            src_url = img_jpg.get('src')

            #Mere the base url with the image source url
            img_url = url + src_url
            
            #Update the url list

            img_h_soup_info_url.append(img_url)
            
            #set browser back to url for a new name (new hemisphere)

            browser.visit(url)

        #Create list of dictionaries

        for x in range(len(img_h_soup_info_name)):
            hemisphere_image_dict = {"title": img_h_soup_info_name[x], "img_url": img_h_soup_info_url[x]}
            hemi_list.append(hemisphere_image_dict)

    except AttributeError:
        return None

    return  hemi_list






    

