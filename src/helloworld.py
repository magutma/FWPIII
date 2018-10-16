import requests
from bs4 import BeautifulSoup

#TinyDB_Zeug

def max_seitenzahl_hotels():
        url = 'https://www.tripadvisor.de/Hotels-g187309-Munich_Upper_Bavaria_Bavaria-Hotels.html'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"html.parser")
        pageNumbers = int(soup.find('div', class_= 'pageNumbers').find(class_='pageNum last taLnk ').text)
        return(int(pageNumbers)*30)
    
def max_seitenzahl_bewertungen(item_url):
        source_code = requests.get(item_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"html.parser")
        pageNumbers = int(soup.find('div', class_= 'pageNumbers').find(class_='pageNum last taLnk ').text)
        print(pageNumbers)
        return (pageNumbers)

def trip_spider(max_pages):
    page = 30
    while page <= max_pages:
        url = 'https://www.tripadvisor.de/Hotels-g187309-oa' + str(page) + '-Munich_Upper_Bavaria_Bavaria-Hotels.html'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"html.parser")
        for link in soup.findAll('a', {'class': 'property_title prominent '}):
           href = 'https://www.tripadvisor.de' + link.get('href')
           title = link.string
           print (title)
           print(href)
           get_single_item_data(href)
           get_single_textrating(max_seitenzahl_bewertungen(href)*5, href)
           #(max_seitenzahl_bewertungen(href)*5, href)
        page += 30
        
def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,"html.parser")
    for item_name in soup.findAll('span', {'class': 'overallRating'}):
        print(item_name.text)

def get_single_textrating(max_pagesII, href):
    pageII = 5
    while pageII <= max_pagesII:
        hrefII, hrefIII = href.split("Reviews",1)
        hrefIIII = hrefII + "Reviews-or" + str(pageII) + hrefIII
        #href II = href.split ("")
        #url =  href #'https://www.tripadvisor.de/Hotel_Review-g187309-d1835007-Reviews-or' + str(pageII) + '-LetoMotel_Muenchen_Moosach-Munich_Upper_Bavaria_Bavaria.html'
        #print (href)
        source_code = requests.get(hrefIIII)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"html.parser")
        for item_name in soup.findAll('p', {'class': 'partial_entry'}):
            print (item_name.text)
            print ("______________________________")
        pageII +=5
        
trip_spider(max_seitenzahl_hotels())