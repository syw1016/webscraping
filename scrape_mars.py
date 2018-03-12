import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

def scrape():
  executable_path = {"executable_path": "chromedriver"}
  browser = Browser("chrome", **executable_path, headless=False)

  # scrape latest news
  nasa = "https://mars.nasa.gov/news/"
  browser.visit(nasa)
  time.sleep(1)

  html = browser.html
  soup = BeautifulSoup(html, "html.parser")

  latest_news = soup.find("li", class_="slide")

  news_title = latest_news.find("div", class_="content_title").a.text
  news_p = latest_news.find("div", class_="article_teaser_body").text

  # scrape image
  mars = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
  browser.visit(mars)
  time.sleep(1)

  button = browser.find_by_id("full_image")
  button.click()
  time.sleep(1)

  button = browser.find_by_text('more info     ')
  button.click()
  time.sleep(1)

  html = browser.html
  soup = BeautifulSoup(html, "html.parser")

  featured_image_url = "https://www.jpl.nasa.gov" + soup.find("img", class_="main_image")['src']

  # scrape weather
  twitter = "https://twitter.com/marswxreport?lang=en"
  browser.visit(twitter)
  time.sleep(1)

  html = browser.html
  soup = BeautifulSoup(html, "html.parser")

  mars_weather = soup.find("p", class_="tweet-text").text

  # scrape table
  url = "http://space-facts.com/mars/"
  dfs = pd.read_html(url)

  fact = dfs[0]
  fact.columns = ['description', 'value']
  mars_fact = fact.to_html(index=False)

  # scrape hemispheres
  hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
  browser.visit(hemi)
  time.sleep(1)

  hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    {"title": "Cerberus Hemisphere", "img_url": "..."},
    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    {"title": "Syrtis Major Hemisphere", "img_url": "..."},
  ]

  for hemisphere in hemisphere_image_urls:
    link = browser.find_by_text(hemisphere["title"] + " Enhanced")
    link.click()
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    hemisphere["img_url"] = soup.find("div", class_="downloads").a['href']
    browser.back()
    time.sleep(1)

  return {"news_title": news_title, "news_p": news_p, "mars_fact": mars_fact, "featured_image_url": featured_image_url, "mars_weather": mars_weather, "hemisphere_image_urls": hemisphere_image_urls}