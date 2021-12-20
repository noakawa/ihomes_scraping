import mysql.connector
import logging
import private_info

logging.basicConfig(filename='home.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


class Creation:

    def __init__(self):

        self.mydb = mysql.connector.connect(
            host=private_info.HOST,
            user=private_info.USER,
            password=private_info.PASS
        )

        self.mycursor = self.mydb.cursor()

    def exist(self):
        try:
            self.mycursor.execute("CREATE DATABASE ihomes")
            logging.info("Database created successfully")
            return False
        except mysql.connector.errors.DatabaseError:
            return True

    def drop(self):
        """This function is used in case we want to drop te database"""
        try:
            self.mycursor.execute("DROP DATABASE ihomes")
        except mysql.connector.errors.DatabaseError:
            logging.info("Database did not exist")

    def create_tables(self):
        self.mycursor.execute("USE ihomes")

        self.mycursor.execute(''' CREATE TABLE `Property` (
          `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
          `link` varchar(255) UNIQUE,
          `sale_or_rent` varchar(255),
          `conditions` varchar(255),
          `type_of_property_id` int,
          `floor_in_building` int,
          `floor` int,
          `rooms` int,
          `built_area` int,
          `furnished` varchar(255),
          `first_listed` datetime,
          `city_id` int,
          `longitude` float,
          `latitude` float,
          `number_of_restaurant` int
        ) ''')
        print("Table created successfully")
        logging.info("Table 'Property' created successfully")

        self.mycursor.execute(''' CREATE TABLE `Type_of_property` (
          `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
          `type` varchar(255) UNIQUE
        ) ''')
        print("Table created successfully")
        logging.info("Table 'Type_of_property' created successfully")

        self.mycursor.execute(''' CREATE TABLE `Price` (
          `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
          `property_id` int,
          `date_of_today` datetime,
          `price` float
        ) ''')
        print("Table created successfully")
        logging.info("Table 'Price' created successfully")

        self.mycursor.execute(''' CREATE TABLE `Cities` (
          `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
          `city_name` varchar(255) UNIQUE
        ) ''')
        print("Table created successfully")
        logging.info("Table 'Cities' created successfully")

        self.mycursor.execute('ALTER TABLE `Price` ADD FOREIGN KEY (`property_id`) REFERENCES Property(`id`)')

        self.mycursor.execute(
            'ALTER TABLE `Property` ADD FOREIGN KEY (`type_of_property_id`) REFERENCES `Type_of_property` (`id`)')

        self.mycursor.execute('ALTER TABLE `Property` ADD FOREIGN KEY (`city_id`) REFERENCES `Cities` (`id`)')

        self.mycursor.close()
        print('Database Closed')
        logging.info('Database Closed')
