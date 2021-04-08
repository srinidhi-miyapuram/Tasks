from googlesearch import search

global links
links = []

result = search(query='buy cbd products online',tld='com',lang='en',num=20,stop=20,pause=2)
for link in result:
    links.append(link)
print(links)

