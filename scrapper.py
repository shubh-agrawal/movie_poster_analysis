from bs4 import BeautifulSoup
from urllib import urlretrieve
import urlparse
import requests
import re
import urllib2
import time
from bs4 import BeautifulSoup

list_link = raw_input("Paste the link here for the list: ")
folder = raw_input("folder path: ")

page = urllib2.urlopen(list_link)
soup = BeautifulSoup(page)
print "here"
images = soup.findAll("div",{"class":"image"})
print images
for img in images:
	img_url = img.img['src']
	file_name = img.img['alt']
	file_name = file_name[9:-1]	
	print img_url
	with open(folder + file_name + ".jpg","wb") as f:
		f.write(urllib2.urlopen(img_url).read())
	time.sleep(0.20)

