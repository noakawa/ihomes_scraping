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
    if len(get_city_id(city)) == 0:
        mycursor.execute(''' INSERT INTO Cities 
            (city_name)
            VALUES ('%s')''' % city)
    else:
        return


def insert_type(type_of_property):
    if len(get_type_of_property_id(type_of_property)) == 0:
        mycursor.execute(''' INSERT INTO Type_of_property
            (type)
            VALUES ('%s')''' % type_of_property)
    else:
        return


def insert_property(link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
                    furnished, first_listed, city_id, conditions):
    if len(get_property_id(link)) == 0:
        query = ''' INSERT INTO Property 
        (link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
                        furnished, first_listed, city_id, conditions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        record = (
            link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
            furnished, first_listed, city_id, conditions
        )
        mycursor.execute(query, record)
    else:
        return


def insert_price(property_id, date_of_today, price):
    if len(get_price_id(property_id, price)) == 0:
        query = ''' INSERT INTO Price 
            (property_id, date_of_today, price)
            VALUES (%s, %s, %s)'''
        record = (property_id, date_of_today, price)
        mycursor.execute(query, record)
    else:
        return


def get_city_id(city):
    mycursor.execute(f''' SELECT id FROM Cities 
            WHERE city_name = ('%s')''' % city)
    return mycursor.fetchall()


def get_type_of_property_id(prop_type):
    mycursor.execute(f''' SELECT id FROM Type_of_property
            WHERE type = ('%s')''' % prop_type)
    return mycursor.fetchall()


def get_property_id(link):
    mycursor.execute(f''' SELECT id FROM Property
            WHERE link = ('%s')''' % link)

    return mycursor.fetchall()


def get_price_id(property_id, price):
    mycursor.execute(f''' SELECT id FROM Price
                WHERE property_id = ('%s') and price = ('%s') ''' % (property_id, price))

    return mycursor.fetchall()


def commit():
    mydb.commit()

# data = os.system("python web_scrap.py -c ak")
# print(data)
