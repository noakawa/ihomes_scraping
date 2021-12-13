import mysql.connector
import private_info
import logging

logging.basicConfig(filename='home.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


class Database:
    def __init__(self):

        self.mydb = mysql.connector.connect(
            host=private_info.HOST,
            user=private_info.USER,
            password=private_info.PASS,
            database="ihomes"
        )

        self.mycursor = self.mydb.cursor()

    def commit(self):
        self.mydb.commit()

    def insert_city(self, city):
        """
        This functions inserts a row in the table City if the city does not exist.
        :param city: name of the city
        """

        if len(self.get_city_id(city)) == 0:
            self.mycursor.execute(''' INSERT INTO Cities 
                (city_name)
                VALUES ('%s')''' % city)
            logging.info(f'{city} inserted')
        else:
            logging.info(f'{city} already in data base')
            return

    def insert_type(self, type_of_property):
        """
        This functions inserts a row in the table Type_of_property if the type_of_property does not exist.
        :param type_of_property: type of property
        """

        if len(self.get_type_of_property_id(type_of_property)) == 0:
            self.mycursor.execute(""" INSERT INTO Type_of_property
                (type)
                VALUES ('%s')""" % type_of_property)
            logging.info(f'{type_of_property} inserted')
        else:
            logging.info(f'{type_of_property} already in data base')
            return

    def insert_property(self, link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
                        furnished, first_listed, city_id, conditions, latitude, longitude, number_of_restaurant):
        """
        This functions inserts a row in the table Property if the property that corresponds to the link does not exist in
        the table.
        """

        if len(self.get_property_id(link)) == 0:
            query = ''' INSERT INTO Property 
            (link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
                            furnished, first_listed, city_id, conditions, latitude, longitude, number_of_restaurant)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            record = (
                link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
                furnished, first_listed, city_id, conditions, latitude, longitude, number_of_restaurant
            )
            self.mycursor.execute(query, record)
            logging.info(f"property with link '{link}' inserted")
        else:
            logging.info(f"property with link '{link}' already in data base")
            return

    def insert_price(self, property_id, date_of_today, price):
        """
        This functions inserts a row in the table Price if the input price is different from the price that corresponds
        to the input property id and update the date of today according to the input date_of_today.
        :param property_id: id of the property
        :param date_of_today: today's date
        :param price: price of the property
        """

        if len(self.get_price_id(property_id, price)) == 0:
            query = ''' INSERT INTO Price 
                (property_id, date_of_today, price)
                VALUES (%s, %s, %s)'''
            record = (property_id, date_of_today, price)
            self.mycursor.execute(query, record)
            logging.info(f'price for property id {property_id} inserted')
        else:
            logging.info(f"price for property id {property_id}' already in data base")
            return

    def get_city_id(self, city):
        """
        This functions return the id of the corresponding city in the table Cities.
        :param city: name of the city
        """

        self.mycursor.execute(f''' SELECT id FROM Cities 
                WHERE city_name = ('%s')''' % city)
        return self.mycursor.fetchall()

    def get_type_of_property_id(self, prop_type):
        """
        This functions return the id from table Type_of_property according to the given type of property.
        :param prop_type: type of property
        """

        self.mycursor.execute(f''' SELECT id FROM Type_of_property
                WHERE type = ('%s')''' % prop_type)
        return self.mycursor.fetchall()

    def get_property_id(self, link):
        """
        This functions return the id from table Property according to the given type of link.
        :param link: link of a property
        """

        self.mycursor.execute(f''' SELECT id FROM Property
                WHERE link = ('%s')''' % link)

        return self.mycursor.fetchall()

    def get_price_id(self, property_id, price):
        """
       This functions return the id from table Price according to the given property id and price.
       :param property_id: id of property
       :param price: price of a property
       """

        self.mycursor.execute(f''' SELECT id FROM Price
                        WHERE property_id = ('%s') and price = ('%s') ''' % (property_id, price))

        return self.mycursor.fetchall()
