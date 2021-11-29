import mysql.connector
import logging
import private_info

logging.basicConfig(filename='home.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)

mydb = mysql.connector.connect(
    host=private_info.HOST,
    user=private_info.USER,
    password=private_info.PASS
)

mycursor = mydb.cursor()

try:
    mycursor.execute("CREATE DATABASE ihomes")
except mysql.connector.errors.DatabaseError:
    mycursor.execute("DROP DATABASE ihomes")
    mycursor.execute("CREATE DATABASE ihomes")

mycursor.execute("USE ihomes")

mycursor.execute(''' CREATE TABLE `Property` (
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
  `city_id` int
) ''')
print("Table created successfully")
logging.info("Table 'Property' created successfully")

mycursor.execute(''' CREATE TABLE `Type_of_property` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `type` varchar(255) UNIQUE
) ''')
print("Table created successfully")
logging.info("Table 'Type_of_property' created successfully")

mycursor.execute(''' CREATE TABLE `Price` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `property_id` int,
  `date_of_today` datetime,
  `price` int
) ''')
print("Table created successfully")
logging.info("Table 'Price' created successfully")

mycursor.execute(''' CREATE TABLE `Cities` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `city_name` varchar(255) UNIQUE
) ''')
print("Table created successfully")
logging.info("Table 'Cities' created successfully")

mycursor.execute('ALTER TABLE `Price` ADD FOREIGN KEY (`property_id`) REFERENCES Property(`id`)')

mycursor.execute('ALTER TABLE `Property` ADD FOREIGN KEY (`type_of_property_id`) REFERENCES `Type_of_property` (`id`)')

mycursor.execute('ALTER TABLE `Property` ADD FOREIGN KEY (`city_id`) REFERENCES `Cities` (`id`)')

mycursor.close()
print('Database Closed')
logging.info('Database Closed')
