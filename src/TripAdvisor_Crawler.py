import requests
from bs4 import BeautifulSoup
import mysql.connector
import re
from distributed.utils_test import div

connection = mysql.connector.connect(host='localhost',
                         database='demo',
                         user='demo',
                         password='123')

db_Info = connection.get_server_info()
print("Connected to MySQL database... MySQL Server version on ",db_Info)
cursor = connection.cursor()

# Methode um Daten in ta_hotel einzufügen
def store_hotel_data (title,href,single_item_data):
    cursor.execute("INSERT INTO ta_hotel (title, href, single_item_data) VALUES (%s,%s,%s)",(title,href,single_item_data))
    connection.commit()
    #cursor.execute("Select * from ta_hotel;")
    record = cursor.fetchone()
    #print ("Your connected to - ", record)

# Methode um Daten in ta_bewertungen einzufügen
def store_bewertungs_data (bewertungen,sterne,HotelID):
    cursor.execute("INSERT INTO ta_bewertungen (bewertungen,sterne,HotelID) VALUES (%s,%s,%s)",(bewertungen,sterne,HotelID))
    connection.commit()
    #cursor.execute("Select * from ta_hotel;")
    record = cursor.fetchone()
    #print ("Your connected to - ", record)

#Crawler
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
           #MySQL Anbindung
           store_hotel_data (title.strip(),href.strip(),get_single_item_data(href))
           HotelID = cursor.lastrowid
           #Bewertungstexte und Sterne werden ausgelesen
           get_single_textrating(max_seitenzahl_bewertungen(href)*5, href, HotelID)
        page += 30

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,"html.parser")
    for item_name in soup.findAll('span', {'class': 'overallRating'}):
        print(item_name.text)
        return (item_name.text)
    
def get_single_textrating(max_pagesII, href, HotelID):
    pageII = 5
    while pageII <= max_pagesII:
        hrefII, hrefIII = href.split("Reviews",1)
        hrefIIII = hrefII + "Reviews-or" + str(pageII) + hrefIII
        source_code = requests.get(hrefIIII)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"html.parser")
        print("__"+hrefIIII)
        #for item_name in soup.findAll('p', {'class': 'partial_entry'}):
        i=0
        for a in soup.findAll('a', attrs={'href': re.compile("^/ShowUserReviews-")}):
            hrefIIIII = "http://www.tripadvisor.de/"+ a['href']
            print (hrefIIIII)
            source_codeI = requests.get(hrefIIIII)
            plain_textI = source_codeI.text
            soupI = BeautifulSoup(plain_textI,"html.parser")
            for item_name in soupI.findAll('span', {'class': 'fullText'}):
                bewertungen = item_name.text
                print(item_name.text)
                #MySQL Anbindung
                #store_bewertungs_data(bewertungen,HotelID)
                containers = soup.findAll("div",{"class":"ui_column is-9"})
                for container in containers:
                    rating = container.span["class"]
                    a, b = str(rating).split(" ",1)
                    c = b
                    d, e = (c.split("_",1))
                    f, g = (e.split("'"))
                    sterne = (int(f)/10)
                    print (int(f)/10)
                    #MySQL Anbindung
                    store_bewertungs_data(bewertungen,sterne,HotelID)
                    #print("Rating: ", rating)
                    soup = soupI
                    print ("______________________________")
                    break
            #Nur 5 Bewertungen pro Seite die Suche nach HTML Links abbrechen
            i+=1
            if i==5:
                break
        pageII +=5
        
trip_spider(max_seitenzahl_hotels())