from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time
import re

# Set up chromedriver (Mac Users)
def init_browser():
	executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
	return Browser("chrome", **executable_path, headless=False)
	
# Create mars_data dict that we can insert into mongoDB
mars_info = {}
	
# Mars News
def scrape_info():
	
    # Initiate the browser
	browser = init_browser()
    	

	# NASA Mars News
	url_news = "https://mars.nasa.gov/news/"
	browser.visit(url_news)
		
	html_news = browser.html
	soup = BeautifulSoup(html_news, "html.parser")
		
	news_title = soup.find("div", class_ = "content_title").text
	news_paragraph = soup.find("div", class_ = "rollover_description_inner").text

	# here
    mars_info["news_title"] = news_title
	mars_info["news_paragraph"] = news_paragraph 

	
	# JPL Mars Space Images - Featured Image
	url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url_img)
	
	html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

	partial_img_url = soup.find("article")["style"].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = 'https://www.jpl.nasa.gov' + partial_img_url

	# here
    mars_info["featured_image_url"] = featured_image_url
	
		
	# Mars Weather on Twitter
	url_weather = "https://twitter.com/marswxreport?lang=en"
	browser.visit(url_weather)

	html = browser.html
    soup = BeautifulSoup(html, "html.parser")
	
	mars_tweets = [soup.find_all('p', class_="TweetTextSize"), soup.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")]
	
    for tweets in mars_tweets:
        mars_tweet = tweets
        
    for tweet in mars_tweet:
        if 'InSight' in tweet.text:
            mars_weather = tweet.text
            if tweet.a in tweet:
                mars_weather = mars_weather.strip(tweet.a.text)
            break
	# here
	mars_info["mars_weather"] = mars_weather
	


	# Mars Facts
	url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)

	facts_table = pd.read_html(url_facts)

    facts_df = facts_table[0]
    facts_df.columns = ['Facts', 'Values']

    facts_df['Facts'] = facts_df['Facts'].str.replace(':', '')
    facts_df.set_index("Facts", inplace=True)
    
    facts_html = facts_df.to_html()

	# here
	mars_info["mars_facts"] = mars_facts

	
	# Mars Hemispheres
	url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url_hemisphere)
	
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
	
	hemispheres = hem_soup.find_all("div", class_="item")

	hemispheres_info = []

    main_url = "https://astrogeology.usgs.gov"

    for i in hemispheres:
        title = i.find("h3").text
        img_link = i.find("a", class_="itemLink product-item")["href"]
        
        browser.visit(main_url + img_link)
        
        hemisphere_html = browser.html
        web_info = BeautifulSoup(hemisphere_html, "html.parser")
        
        hemisphere_url = main_url + web_info.find("img", class_="wide-image")["src"]
        
        hemispheres_info.append({"title" : title, "hemisphere_url" : hemisphere_url})
	# here
	mars_info["hemispheres_info"] = hemispheres_info
	

	# Close the browser after scraping
	browser.quit()
	

	return mars_info
	
	