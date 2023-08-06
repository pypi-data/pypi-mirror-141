# !/usr/bin/env Python3
# import Module
import requests as req from bs4 
import BeautifulSoup as bs

# Function Whois Domain
def whois_domain(domain): url = 
  req.get(f"https://www.shopify.com/tools/whois/search?query={domain}") 
  soup = bs(url.text, 
  "html.parser") sortir = 
  soup.find("section", 
  {"class":"record-container"}) 
  sort = 
  sortir.find("pre").get_text() 
  return sort
# Function Whois IP
def whois_ip(ipAddress): url = 
  req.get(f"https://dnschecker.org/ip-whois-lookup.php?query={ipAddress}") 
  soup = bs(url.text, 
  "html.parser") sortir = 
  soup.find("li", 
  {"class":"list-group-item"}) 
  return sortir
  
import os, time
# Definisi Save Docoment
def 
save_fileText(fileName,Document,docType):
  ext = ("doc","pdf","csv","txt")
  # fileName
  if docType in ext: with 
    open(fileName+"."+docType, 
    "w") as f:
      f.write(Document) f.close()
      
    print("[BERHASIL] File anda 
    berhasil kami buat :-)")
  else: print("[GAGAL] File 
    dokumen yang anda masukkan 
    tidak dapat kami baca!")
def 
save_fileImage(fileName,Document,docType):
  ext = 
  ("png","jpg","jpeg","webp","svg","gif")
  # fileName
  if docType in ext: with 
    open(fileName+"."+docType, 
    "wb") as f:
      f.write(Document) f.close()
      
    print("[BERHASIL] File anda 
    berhasil kami buat :-)")
  else:
    print("[GAGAL] File dokumen yang anda masukkan tidak dapat kami baca!")
