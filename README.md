# Data mining iHomes

Gather data from iHomes, Israel's real estates online listing.

## Getting Started

This project contains 8 files: config.py, requirements.txt, web_scrap.py, out_of_scrap.py, db_creation.py, 
db_implementation.py, private_info.py, ERD_ihomes.sql and README.md

There are implemented to scrap data from iHomes website 'https://www.ihomes.co.il/s/tel-aviv-yafo' 
and gather information about properties in cities in Israel

It is implemented using bs4 and grequests 

### Installation

1. Create a virtual environment

2. Downloads the 8 files into a folder

3. Install the packages into your virtual environment from requirements.txt:

```
pip install -r requirements.txt
```

4. Fill the file private_info.py with your connection info for mysql and your API Key to access Google API. 

5. Run the following command to create the database
```
python3 db_creation.py 
```

6. Run the following command from terminal to get help of what arguments are necessary
```
python3 web_scrap.py -h
```

### Implementation of config.py

######config.py is a configuration file that has five variable:


* URL 

The url of iHomes website

* BATCHES

The number of batches used for the grequest 

* HE_TO_EN

A dictionary used to translate words from hebrew to
english. iHomes is originally an israeli website implemented in hebrew with available english translation, scraping data
using grequest and bs4 do not automatically translate all the data, therefore we created HE_TO_EN to make the translation

* ATTRIBUTES 

The properties attribute we want to scrap from the pages. 

Those variables are called in web_scrap.py and referenced as:

```
config.[VARIABLE_NAME]
```

* OPTIONS

The options the user select between sell or rent in the command line

* CITIES

A dictionary used to match the inputs values of cities to the cities

* RADIUS

Defines the distance (in meters) within which to return the number of restaurants around the given propertie.

### Implementation private_info.py

private_info.py contains the required information to establish a connection with MySQL. It also contains a KEY to connect to the Google API

* HOST
* USER
* ROOT
* KEY

### Implementation out_of_scrap.py

out_of_scrap.py contain a python code which calls main() and seven other functions

* access_url(response, url)

This function send a logging to access an url

* url_city(city)

This function returns the url of the specific city

* list_url_cities(cities)

This function returns a list of urls for each city according to the input list of cities.

* max_pages(city)

This function get as input the name of a city to scrap and return the maximum number of pages of link.

* pages_to_list(city, no_of_page)

This function returns a list of links of pages in the website depending on the input number and name of the city.

* links_to_soup(urls, batches=config.BATCHES)

This function will return a list of soup objects for each input urls, using grequest and the input batches number.

* get_sub_page(urls, batches=config.BATCHES)

This function receives the links of all pages and returns a list of all subpages urls.
Using grequest and the input batches number to open the pages.

### Implementation web_scrap.py

web_scrap.py contain a python code which calls main(), get the arguments from the users and use 13 other functions to scrap the required data.

* get_data(city, soup, sub_link, sell_or_rent=False, max_price=False, min_date=False)

This function gets the subpage urls and return a dictionary with all the data for the list of attributes. 
If no list_of_attributes given, automatically return all the attributes found.
If no data are available for a specific attribute the function will describe it as None.

* price_shekels(price)

This function converts every prices in shekel.

* get_price(soup, all_data, sub_link)

This function returns a dictionary updated with the prices (all in shekel).

* get_ll(soup, all_data, sub_link)

This function returns the dictionary updated with the longitude and latitude of a property.

* get_features(all_data, features, sub_link)

This function returns the dictionary updated with the features.

* get_type_of_property_en(feature, sub_link)

This function returns the translation in english of the type of property

* m2_to_int(feature)

This function keeps the integers from a string.

* subset_data(all_data_n, list_of_attributes, sub_link, city)

This function returns a dictionary with the specific data asked.

* valid_date(s)

This function will raise an error if the format of input date is incorrect.

* print_output(s, p, d, city)

This function print the scraped data. 

* get_args()

This function returns the arguments from the command line.

* get_number_of_restaurants(latitude, longitude, radius)

This function returns the number of restaurant in a certain radius around a point defined by its latitude and longitude.

* insert_into_db(data)

This function inserts the data from a dictionary to the database calling the Database class.

In addition, the code will create a file home.log with the logging and stdout.log with the output.

### Implementation db_creation.py

db_creation.py creates, using Mysql queries a database with four tables.
First it establish a connection with MySQL, then creates a new database.

You need to have access to the root user, in order to creates and implement the MySQL database. 

We used private_informaton to store our information in a private file, however you should use your own login information to run the code.

### Implementation db_implementation.py

Create a class Database which has 10 functions.
This class is implemented to insert the data we scrap into the MySQL database created in db_creation.py.

* __init__(self):

Creates a mysql connector and a cursor.

* commit(self)

Commit the inserts queries to makes the changes of the database permanent and visible.

* insert_city(self, city)

This functions inserts a row in the table City if the city does not exist

* insert_type(self, type_of_property)

This functions inserts a row in the table Type_of_property if the type_of_property does not exist.

* insert_property(self, link, sale_or_rent, type_of_property_id, floor_in_building, floor, rooms, built_area,
                    furnished, first_listed, city_id, conditions, latitude, longitude, number_of_restaurant)
                    
This functions inserts a row in the table Property if the property that corresponds to the link does not exist in the table.
 
 * insert_price(self, property_id, date_of_today, price)
 
 This functions inserts a row in the table Price if the input price is different from the price that corresponds to the input property id 
 and update the date of today according to the input date_of_today.
 
 * get_city_id(self, city)
 
 This functions returns the id of the input city from table Cities
 
 * def get_type_of_property_id(self, prop_type)
 
 This functions return the id from table Type_of_property according to the given type of property.
 
 * get_property_id(self, link)
 
 This functions return the id from table Property according to the given type of link.
 
 * get_price_id(self, property_id, price)
 
 This functions return the id from table Price according to the given property id and price.

### Data Base 
The DataBase has 4 tables:

1. Property - store information for each property. 
  - id :  unique identification number of the property; primary key for this table
  - link :  website link of each property
  - sale_or_rent : if the property is for sale or rent
    - Sell
    - Rent
  - condition : condition of the property
  - type_of_property_id : foreign key to the table Type_of_property with a one to many relation
  - floor_in_building: total number of floors in the building
  - floor: floor of the property
  - rooms: number of rooms in the property
  - built_area: gross area of the property in m^2 
  - furnished: if the property is furnished or not
    - Yes
    - No
  - first_listed: date the property was listed for the first time
  - city_id: foreign key to the table City with a one to many relation
  - longitude: of the point representing the property
  - latitude: of the point representing the property
  - number_of_restaurant: number of restaurant around the property within a radius of 500 meters.
 
2. Type_of_property 
  - id: unique id for each type of property; primary key for this table
  - type: type of property 
    - Penthouse
    - House
    - Garden Apartment
    - Duplex
    - Semi-detatched
    - Villa
    - Cottage
    - Plot
    - Studio
    - Office
    - Mini Penthouse
    - Apartment
    - building
    - Shop

3.  Price: store the price of each property and the curent date of price estimation. Every time the prices change it adds a row with new price and the date.
  - id: unique id for each type of property; primary key for this table
  - property_id: foreign key to the table Pice; it's a one to many relation tothe table Propety
  - date_of_today: the date of today
  - price: price for the property according to property_id

4. Cities : in this table we'll store the name of each city were the property is located. 
 - id: unique id for each city; primary key for this table
 - city_name: name of city
   - raanana
   - jerusalem
   - tel-aviv-yafo
   - herzliya
   - ashdod
   - haifa
   - netanya
   - ashkelon
 
### ERD_ihomes.sql

MySQL code that creates our database structure.

## Authors

Noa Kawa Keren Portugais


