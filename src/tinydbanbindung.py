import mysql.connector
from mysql.connector import Error
import sys,time
from django.db import models




#try:
connection = mysql.connector.connect(host='localhost',
                          database='demo',
                          user='demo',
                          password='123')
#if connection.is_connected():
db_Info = connection.get_server_info()
print("Connected to MySQL database... MySQL Server version on ",db_Info)
cursor = connection.cursor()

#cursor.execute("insert into ta_hotel ")
#INSERT INTO ta_hotel VALUES(2,"asdf","asdf",1,"asdf")
#sql = "Insert INTO ta_hotel (HotelID, title, href, single_item_data, single_textrating) VALUES (Highway 21)"
#val = ("Highway 21")
#cursor.execute(sql, val)
def store_data (title,href,single_item_data):
    cursor.execute("INSERT INTO ta_hotel (title, href, single_item_data) VALUES (%s,%s,%s)",(title,href,single_item_data))
    connection.commit()
    #cursor.execute("Select * from ta_hotel;")
    record = cursor.fetchone()
    print ("Your connected to - ", record)

def store_text (bewertungen,HotelID):
    cursor.execute("INSERT INTO ta_bewertungen (bewertungen, HotelID) VALUES (%s,%s)",(bewertungen,HotelID))
    connection.commit()
    #cursor.execute("Select * from ta_hotel;")
    record = cursor.fetchone()
    print ("Your connected to - ", record)

def test():
    page = 1
    while page <= 10:
        title = "HotelNameWirdUebergeben"
        href = "WebAdresseWirdUebergeben"
        single_item_data = "BewertungWirdUebergeben"
        bewertungen=  "DiesIsteineBeispielbewertungsText"
        store_data (title,href,single_item_data)
        #global HotelID
        HotelID = cursor.lastrowid
        pageII= 1
        while pageII <= 10:
            store_text(bewertungen,HotelID)
            pageII+=1
        page +=1
 
test()

if(connection.is_connected()):
    cursor.close()
    connection.close()
    print("MySQL connection is closed",)