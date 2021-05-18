from googlesearch import search

global links
links = []
search_name = input("Enter what you want to search here : ")

result = search(query=search_name ,tld='com',lang='en',num=20,stop=20,pause=2)
for link in result:
    links.append(link)
print(links)

