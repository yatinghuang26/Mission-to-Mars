# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

html = browser.html
hemisphere_soup = soup(html, 'html.parser')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
hemisphere_image_titles = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Find each item first
full_results = hemisphere_soup.find('div', class_='collapsible results')
full_items = full_results.find_all('div', class_='item')

# Then iterate through each item to find the url and title
for item in full_items:
    #print(f'1\n{item}')
    
    # Retrieve the PARTIAL url first
    website = 'https://marshemispheres.com/'  # The first part of the url is https://marshemispheres.com/
    url = website + item.find('a', href = True)['href']
    hemisphere_image_urls.append(url)         # Add it to the url list
    
    
    # Retrieve the title 
    find_title = item.find('div', class_='description')
    title = find_title.find('h3').text
    hemisphere_image_titles.append(title)
    
print(hemisphere_image_urls)
print(hemisphere_image_titles)

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_list = []

for x in range(0, len(hemisphere_image_urls)):
    hemisphere_dict = {}
    hemisphere_dict['img_url'] = hemisphere_image_urls[x]
    hemisphere_dict['title'] = hemisphere_image_titles[x]
    hemisphere_list.append(hemisphere_dict)

print(hemisphere_list)

# 5. Quit the browser
browser.quit()