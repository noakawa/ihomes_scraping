import mysql.connector
import private_info

mydb = mysql.connector.connect(
    host=private_info.HOST,
    user=private_info.USER,
    password=private_info.PASS,
    database="ihomes"
)

mycursor = mydb.cursor()


def insert_city(city):
    """
    This functions inserts a row in the table City if the city does not exist.
    :param city: name of the city
    """

    if len(get_city_id(city)) == 0:
        mycursor.execute(''' INSERT INTO Cities 
            (city_name)
            VALUES ('%s')''' % city)
    else:
        return


def insert_type(type_of_property):
    """
    This functions inserts a row in the table Type_of_property if the type_of_property does not exist.
    :param type_of_property: type of property
    """

    if len(get_type_of_property_id(type_of_property)) == 0:
        mycursor.execute(''' INSERT INTO Type_of_property
            (type)
            VALUES ('%s')''' % type_of_property)
    else:
        return


def insert_property(link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
                    furnished, first_listed, city_id, conditions):
    """
    This functions inserts a row in the table Property if the property that corresponds to the link does not exist in
    the table.
    """

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
    """
    This functions inserts a row in the table Price if the input price is different from the price that corresponds
    to the input property id and update the date of today according to the input date_of_today.
    :param property_id: id of the property
    :param date_of_today: today's date
    :param price: price of the property
    """

    if len(get_price_id(property_id, price)) == 0:
        query = ''' INSERT INTO Price 
            (property_id, date_of_today, price)
            VALUES (%s, %s, %s)'''
        record = (property_id, date_of_today, price)
        mycursor.execute(query, record)
    else:
        return


def get_city_id(city):
    """
    This functions return the id of the corresponding city in the table Cities.
    :param city: name of the city
    """

    mycursor.execute(f''' SELECT id FROM Cities 
            WHERE city_name = ('%s')''' % city)
    return mycursor.fetchall()


def get_type_of_property_id(prop_type):
    """
    This functions return the id from table Type_of_property according to the given type of property.
    :param prop_type: type of property
    """

    mycursor.execute(f''' SELECT id FROM Type_of_property
            WHERE type = ('%s')''' % prop_type)
    return mycursor.fetchall()


def get_property_id(link):
    """
    This functions return the id from table Property according to the given type of link.
    :param link: link of a property
    """

    mycursor.execute(f''' SELECT id FROM Property
            WHERE link = ('%s')''' % link)

    return mycursor.fetchall()


def get_price_id(property_id, price):
    """
   This functions return the id from table Price according to the given property id and price.
   :param property_id: id of property
   :param price: price of a property
   """

    mycursor.execute(f''' SELECT id FROM Price
                    WHERE property_id = ('%s') and price = ('%s') ''' % (property_id, price))

    return mycursor.fetchall()


def commit():
    mydb.commit()


