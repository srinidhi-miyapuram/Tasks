import requests
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen

links = ['https://cbdmd.com','https://cbdfx.com','https://premiumjane.com','https://bluebirdbotanicals.com','https://nuleafnaturals.com','https://purekana.com','https://joyorganics.com','https://greenroads.com','https://medterracbd.com','https://justcbdstore.com','https://www.thecbdistillery.com/','https://cbdamericanshaman.com/','https://www.corecbd.com/','https://www.endoca.com/cbd-products/cbd-oil','https://www.bluerivernutrition.com/','https://www.cbdpure.com/','https://fabcbd.com/','https://royalcbd.com/','https://miraflora.co/','https://www.getsabaidee.com/']
global new_links
new_links = set()
for url in links:
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    for tag in soup.findAll("a"):
        href = tag("FAQs" or "Blog")
        new_links.add(url)    
print("links are : ",new_links)