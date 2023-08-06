# !/usr/bin/env/Python3
import requests as req from bs4 
import BeautifulSoup as bs 

def save(fileName, document):
	with open(fileName+".txt","w") as f:
		f.write(""" 
		Your Current Search Results
                =================================================
                ||   Author: ||   TomsDroid || 
                ||   Credit: ||   Skull Cyber 
                ||   Security ~ ||   Indonesia ||
                =================================================\n\n""") 
                f.write(document)

def whois_domain(domain):
	url = req.get(f"https://www.shopify.com/tools/whois/search?query={domain}") 
  	soup = bs(url.text, "html.parser") 
	sortir = soup.find("section", {"class":"record-container"}) 
	sort = sortir.find("pre").get_text()
	return sort

def whois_ip(ipAddress):
	url = req.get(f"https://dnschecker.org/ip-whois-lookup.php?query={ipAddress}") 
	soup = bs(url.text, "html.parser")
	sortir = soup.find("li", {"class":"list-group-item"})
  	return sortir
