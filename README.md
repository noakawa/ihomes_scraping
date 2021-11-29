# Data mining iHomes

Gather data from iHomes, Israel's real estates online listing.

## Getting Started

This project contains 7 files: config.py, requirements.txt, web_scrap.py, out_of_scrap.py, db_creation.py, 
db_implementation.py, private_info.py and README.md

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

4. Fill the file private_info.py with your connection info for mysql

5. Run the following command from terminal to get help of what arguments are necessary
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

* CITIES

A dictionary used to match the inputs values of cities to the cities
### Implementation out_of_scrap.py
out_of_scrap.py contain a python code which calls main() and seven other functions

* access_url(response, url)
This function send a logging to access a url

* url_city(city)
return the url of the specific city

* list_url_cities(cities)
return a list of urls for each city according to the input list of cities

* max_pages(city)
input the nameof a city to scrap and return the maximum number of pages of link

* pages_to_list(city, no_of_page)
return a list of links of pages in the website depending on the input number and name of the city

* links_to_soup(urls, batches=config.BATCHES)
will return a list of soup
objects for each input urls, using grequest and the input batches number

* get_sub_page(urls, batches=config.BATCHES)
This function receives the links of all pages and returns a list of all subpages urls.
Using grequest and the input batches number to open the pages.

### Implementation web_scrap.py

web_scrap.py contain a python code which calls main() and seven other functions

* get_data(city, soup, sub_link, sell_or_rent=False, max_price=False, min_date=False)

get the subpage urls and return a dictionary with all the data for the list of attributes. 
If no list_of_attributes given, automatically return all the attributes found.
If no data are available for a specific attribute the function will describe it as None.

* price_shekels(price)
convert every prices in shekel

* get_price(soup, all_data, sub_link)
returns a dictionary updated with the prices all in shekel

* get_features(all_data, features, sub_link)
returns the dictionary updated with the features

* subset_data(all_data_n, list_of_attributes, sub_link, city)
returns a dictionary with the specific data asked

* valid_date(s)
raise an error if the format of the input date is not correct

* print_output(s, p, d, city)
print the data 

In addition, the code will create a file home.log with the logging and stdout.log with the output.

### Data Base 
The DataBase has 4 tables:

1. Property - store information for each property on the website 
  a. id - unique identification number of the property; primary key for this table
  b. link - website link ofeach property
  c. sale_or_rent - if the property if for sale or to rent
  d. condition - 
  e. type_of_property_id - foreign key to the table Type_of_property with a one to many relation
  f. floor_in_building - how many floor there are in the building of the property
  g. floor
  h. rooms
  i. built_area
  j. furnished
  k.  first_listed
  l. city_id - foreign key to the table City with a one to many relation
 
2. Type_of_property 
  a. id - unique id for each type of property; primary key for this table
  b. type - name of type 

3.  Price - store the price of each property and the curent date of price estimation
  a. id - unique id for each type of property; primary key for this table
  b. property_id - foreign key to the table Pice; it's a one to many relation tothe table Propety
  c. date_of_today 
  d. price - price for the property according to property_id

4. Cities - in this table we'll store the name of each city were the property is located 
 a. id- unique id for each city; primary key for this table
 b. city_name 

## Authors

Noa Kawa Keren Portugais


