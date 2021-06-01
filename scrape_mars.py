#scrape

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser)
    }

    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay 
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    html = browser.html
    news_soup = bs(html, 'html.parser')
  
    try:
        slide_elem = news_soup.select_one('div.list_text')
        
        news_title = slide_elem.find("div", class_="content_title").get_text()
        
        news_p = slide_elem.find(
            "div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p




def mars_facts():
    try:
        df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    df.columns=["Description", "Value"]
    # create table
    return df.to_html(index=False, classes="table table-striped")


def featured_image(browser):
    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
    browser.click_link_by_partial_text('FULL IMAGE')
    html = browser.html
    image_soup = bs(html, 'html.parser')
    # Search for image source
    image_url = image_soup.find("img", class_="fancybox-image").get("src")
    featured_img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_url}'

    return featured_img_url



def hemispheres(browser):
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    html = browser.html
    hem_soup = bs(html, 'html.parser')

    hemisphere_image_urls = []
    # iterate pics
    for i in range(4):
        hemisphere = {}
    
        browser.find_by_css("a.product-item h3")[i].click()
        time.sleep(1)
    
        html = browser.html
        hemi_soup = bs(html, "html.parser")

        hemisphere['img_url'] = hemi_soup.find("a", text="Sample").get("href")
        hemisphere['title'] = hemi_soup.find("h2", class_="title").get_text()

        hemisphere_image_urls.append(hemisphere)

        browser.back()
    
    return hemisphere_image_urls