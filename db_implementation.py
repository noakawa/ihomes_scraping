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
    mycursor.execute(''' INSERT IGNORE INTO Cities 
        (city_name)
        VALUES ('%s')''' % city)


def insert_type(type_of_property):
    mycursor.execute(''' INSERT IGNORE INTO Type_of_property
        (type)
        VALUES ('%s')''' % type_of_property)


def insert_property(link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
                    furnished, first_listed, city_id, conditions):
    query = ''' INSERT IGNORE INTO Property 
    (link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
                    furnished, first_listed, city_id, conditions)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    record = (
        link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
        furnished, first_listed, city_id, conditions
    )
    mycursor.execute(query, record)


def insert_price(property_id, date_of_today, price):
    query = ''' INSERT INTO Price 
        (property_id, date_of_today, price)
        VALUES (%s, %s, %s)'''
    record = (property_id, date_of_today, price)
    mycursor.execute(query, record)


def get_city_id(city):
    mycursor.execute(f''' SELECT id FROM Cities 
            WHERE city_name = ('%s')''' % city)
    return mycursor.fetchall()


def get_type_of_property_id(prop_type):
    mycursor.execute(f''' SELECT id FROM Type_of_property
            WHERE type = ('%s')''' % prop_type)
    return mycursor.fetchall()


def get_property_id():
    mycursor.execute(f''' SELECT last_insert_id()''')
    return mycursor.fetchall()


def commit():
    mydb.commit()

# data = os.system("python web_scrap.py -c ak")
# print(data)
