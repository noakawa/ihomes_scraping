import mysql.connector
import os
import private_info

mydb = mysql.connector.connect(
    host=private_info.HOST,
    user=private_info.USER,
    password=private_info.PASS,
    database="ihomes"
)

mycursor = mydb.cursor()


def insert_city(city):
    mycursor.execute(f''' INSERT INTO Cities 
        (city_name)
        VALUES ({city})''')


def insert_type(type_of_property):
    mycursor.execute(f''' INSERT INTO Cities 
        (type_of_property)
        VALUES ({type_of_property})''')


def insert_property(link, sale_or_rent, condition, type_of_property_id, floor_in_building, floor, rooms, built_area,
                    furnished, first_listed, city_id):
    mycursor.execute(f''' INSERT INTO property 
    (link, sale_or_rent, condition, type_of_property_id, floor_in_building, floor, rooms, built_area, furnished, 
    first_listed, city_id)
    VALUES ({link}, {sale_or_rent}, {condition}, {type_of_property_id}, {floor_in_building}, {floor}, {rooms}, {built_area}, 
            {furnished}, {first_listed}, {city_id})''')


def insert_price(property_id, date_of_today, price):
    mycursor.execute(f''' INSERT INTO Cities 
        (property_id, date_of_today, price)
        VALUES ({property_id}, {date_of_today}, {price})''')

# data = os.system("python web_scrap.py -c ak")
# print(data)
