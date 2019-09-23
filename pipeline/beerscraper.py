import selenium
import re
import json
import nltk
import os
import glob
import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from collections import OrderedDict
from selenium.webdriver.chrome.options import Options  

beerlist = np.loadtxt('../beerfiles/allbeers.txt', dtype='str')
chrome_options = Options()  
chrome_options.add_argument("--headless")  
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(3)

for beer in beerlist:
	driver.implicitly_wait(3)
	driver.get(beer)
	html = driver.page_source
	soup = BeautifulSoup(html, 'lxml')


	# Get # of reviews
	nreviews = soup.find('span', class_='ba-reviews').get_text()
	nreviews = float(nreviews.replace(',', ''))
	if nreviews > 4:
		# Get name, brewery
		n_b = str(soup.find("h1"))[4:]
		name, brewery = n_b.split('<br/><span style="color:#999999; font-size:0.75em;">', 1)
		brewery = brewery.split('<', 1)[0]
		print(name)
		
		# Get score
		try:
			score = soup.find('span', class_='ba-score').get_text()
			score = float(score)
		except AttributeError:
			score = '0'
	
		# Get style
		style = soup.find_all('a', href=re.compile('/beer/style/'))[0].get_text()
		
		# Get ABV
		ABV = soup.find_all('dd', class_='beerstats')[1].get_text()
		ABV = ABV.split('%')[0]  
		try:  
			ABV = float(ABV)
		except ValueError:  
			ABV = 0 
		
		# get words from reviews
		words = ''
		for s in soup.find_all("div", id="rating_fullview_content_2"):
			s = list(s.stripped_strings)[5:]
			words += ' '.join(s[:-4]) + ' '
		# Convert to all lowercase
		words = words.lower()
		# Convert to list of words
		words = words.split()
		# Remove stopwords
		words = [word for word in words if word not in nltk.corpus.stopwords.words	("english")]
		# Remove puncutation
		words = [re.sub(r'[^\w\s]', '', word) for word in words]
		# Remove some particular words that break things
		words = [word for word in words if word not in ['name', 'style', 'brewery', 'rating', '']]
		# Remove numbers
		words = [word for word in words if not word.isdigit()]
		words = pd.DataFrame({'words' : [words]})
	
		attributes = {'name' : name, 'brewery' : brewery, 'style' : style, 'score' : score, 'ABV' : ABV, 'nreviews' : nreviews}
	
		try:
			df = pd.DataFrame(attributes, index=[0])
			df = pd.merge(df, words, how='left', left_index=True, right_index=True	)
		except KeyError:
			print('Key error')
		try:
			df.to_csv('../beers/'+name.replace(' ', '')+'.csv') 
		except FileNotFoundError:
			print('who knows what is wrong')


# Combine all beers
os.chdir(".")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combinedbeers.csv", index=False, encoding='utf-8-sig')



# Remember when grabbing word names to split them
# wordlist = file['words'][0].split(',')
# out = wordlist[0].translate(wordlist[0].maketrans("","", string.punctuation))