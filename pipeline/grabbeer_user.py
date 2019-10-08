import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import re


user = 'LiquidAmber'
# Open web browser and go to style page
driver = webdriver.Chrome()
driver.get('https://www.beeradvocate.com/user/beers/?ba='+user)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')





# Grab URL from each style of beer, filter out misc results
allbeers = soup.select('a[href*=styles]') 
allbeers = allbeers[1:112]

for beer_styles in range(len(allbeers)): 
	allbeers[beer_styles] = str(allbeers[beer_styles]) 
	allbeers[beer_styles] = allbeers[beer_styles].replace('<a href="', 'https://www.beeradvocate.com').split('"', 1)[0]


# Now using all beer styles, grab individual beers from each beer style
beers = []
for beer_style in range(len(allbeers)):
	driver.get(allbeers[beer_style])
	html = driver.page_source

	# Get those pesky broken links out
	if '404 Not Found - Beer Advocate' in html:
		continue

	soup = BeautifulSoup(html, 'lxml')
	beerlist = soup.select('a[href*=profile]') 
	if len(beerlist) == 0:
		continue

	for beer in range(len(beerlist)): 
		beerlist[beer] = str(beerlist[beer]) 
		beerlist[beer] = beerlist[beer].replace('<a href="', 'https://www.beeradvocate.com') .split('"', 1)[0] 

	# Hack to remove brewery data
	beerlist = np.array(np.delete(beerlist, np.arange(1, len(beerlist), 2))).tolist()

	# Add all beer links from every page to one list
	for i in beerlist:
		beers.append(i)


file = open('allbeerlist.txt', 'w')  

for element in beers: 
	file.write(element)
	file.write('\n') 
                                                                   
file.close()                                                           


# GOOD ENOUGH FOR NOW. Yields 5516 beers.
# To do:
# Go to the next page and repeat




 
