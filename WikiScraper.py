from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

def getInternalLinks(bsObj, includeUrl):
	includeUrl = urlparse(includeUrl).scheme+"://"+urlparse(includeUrl).netloc
	internalLinks = []

	for link in bsObj.findAll("a", href = re.compile("^(/|.*"+includeUrl+")")):
		if link.attrs['href'] is not None:
			if link.attrs['href'] not in internalLinks:
				if(link.attrs['href'].startswith("/")):
					internalLinks.append(includeUrl+link.attrs['href'])
				else:
					internalLinks.append(link.attrs['href'])
	return internalLinks

def getRandomExternalLinks(StartingPage):
	html = urlopen(StartingPage)
	bsObj = BeautifulSoup(html,'lxml')
	externalLinks = getExternalLinks(bsObj,urlopen(StartingPage).netloc)
	if len(externalLinks) == 0:
		print('No external links')
		domain = urlparse(StartingPage).scheme+"://"+urlparse(StartingPage).netloc
		internalLinks = getInternalLinks(bsObj, domain)
		return getRandomExternalLinks(internalLinks[random.randint(0,len(internalLinks)-1)])
	else:
		return externalLinks[random.randint(0,len(externalLinks)-1)]

def getExternalLinks(bsObj,excludeUrl):
	externalLinks = []
	for link in bsObj.findAll("a", href = re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
		if link.attrs['href'] is not None:
			if link.attrs['href'] not in externalLinks:
				externalLinks.append(link.attrs['href'])
	return externalLinks

def followExternalLinkOnly(StartingSite):
	externalLink = getRandomExternalLinks(StartingSite)
	print("Random external link is:"+externalLink)
	followExternalLinkOnly(externalLink)


allExtLinks = set()
allIntLinks = set()

def getAllExternalLinks(siteUrl):
	html = urlopen(siteUrl)
	domain = urlparse(siteUrl).scheme+"://"+urlparse(siteUrl).netloc
	bsObj = BeautifulSoup(html, 'lxml')
	internalLinks = getInternalLinks(bsObj,domain)
	externalLinks = getExternalLinks(bsObj,domain)

	for link in externalLinks:
		if link not in allExtLinks:
			allExtLinks.add(link)
			print(link)
	for link in internalLinks:
		if link not in allIntLinks:
			allIntLinks.add(link)
			getAllExternalLinks(link)

allIntLinks.add("http:python.org")
getAllExternalLinks("http://python.org")
followExternalLinkOnly("http://python.org")
