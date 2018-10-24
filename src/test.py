from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup

my_url = 'https://www.tripadvisor.com.sg/Attraction_Review-g293916-d12033454-Reviews-SHOW_DC-Bangkok.html'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div",{"class":"ui_column is-9"})
#print (containers)

for container in containers:
    rating = container.span["class"]
    #comment_container = container.p.contents
    #comment = comment_container[0]
    print("Rating: ", rating)
    #print("Comment: " + comment)
