import requests
from urllib.parse import urlparse, urljoin
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
import colorama
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()
links = []
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set  
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls
# number of urls visited so far will be stored here
total_urls_visited = 0

def crawl(url, max_urls=50):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

def urls(url):
    for href in url:
        print(href)
        count = urlopen(href).getcode()
        print(count)
        if count >= 400 and count < 600:
            msg = MIMEMultipart(_subtype=MIMEText)
            msg.attach(MIMEText(f"Sir, Your {href} page found down."))
            print(msg)
        smtp = smtplib.SMTP('smtp.gmail.com', port='587')
        smtp.ehlo()  # send the extended hello to our server
        smtp.starttls()  # tell server we want to communicate with TLS encryption
        smtp.login('sri@gmail.com', 'Password123')  # login to our email server
        smtp.sendmail('sri@gmail.com',
                      'web@gmail.com',
                      msg.as_string())
        smtp.quit()
if __name__ == "__main__":
    crawl("https://docplus.online/")
    print("[+] Total External links:", len(external_urls))
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total:", len(external_urls) + len(internal_urls)) 
    print("links are : ",internal_urls)
    urls(internal_urls)
    