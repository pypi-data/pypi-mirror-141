# !/usr/bin/env/Python3
import requests as req
from bs4 import BeautifulSoup as bs

def save(fileName, document):
        with open(fileName+".txt", "w") as f:
                f.write("""
                            Your Current Search Results
                =================================================
                ||   Author: TomsDroid                         ||
                ||   Credit: Skull Cyber Security ~ Indonesia  ||
                =================================================\n\n""")
                f.write(document)

        print(f"\033[93m [\033[92mSUCCESS\033[93m] \033[97m File {fileName}.txt berhasi>

def whois_domain(domain):
        data = { "query":domain }
        pages = req.get("https://www.shopify.com/tools/whois/search?",params=data)
        parsing = bs(pages.text, "html.parser")
        cariElement = parsing.find("section", {"class":"record-container"})
        ambilElement = cariElement.find("pre").get_text()
        return ambilElement

def whois_ip(ip):
        pages = req.get(f"https://who.is/whois-ip/ip-address/{ip}")
        parsing = bs(pages.text, "html.parser")
        parse = parsing.find("pre").get_text()
        return parse
