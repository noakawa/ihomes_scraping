# Data mining iHomes

Gather data from iHomes, Israel's real estates online listing.

## Getting Started

This project contains 4 files: config.py, requirements.txt, web_scrap.py and README.md

There are implemented to scrap data from iHomes website 'https://www.ihomes.co.il/s/tel-aviv-yafo' 
and gather information about properties in Tel Aviv only

It is implemented using bs4 and grequests 

### Installation

1. Create a virtual environment

2. Downloads the four files

3. Install the packages into your virtual environment from requirements.txt:

```
pip install -r requirements.txt
```

4. Run web_scrap.py

### Implementation of config.py

######config.py is a configuration file that has five variable:


* URL 

The url of iHomes website


* PAGE: 

The number of web pages from which we'll gather data in this case 51
'https://www.ihomes.co.il/s/tel-aviv-yafo?page=XX' in the previous url we will replace XX with the page number 1-51

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

### Implementation web_scrap.py

web_scrap.py contain a python code which calls main() and four other functions

* pages_to_list(no_of_page) 

return a list of links of pages in the website depending on the input number in our case
number of pages is 51, defined in the config file.

* get_sub_page(urls, batches=config.BATCHES)

This function receives the links of all pages and returns a list of all subpages urls.
Using grequest and the input batches number to open the pages.


* links_to_soup(urls, batches=config.BATCHES)

will return a list of soup
objects for each input urls, using grequest and the input batches number 

* get_data(soup, sub_link, list_of_attributes=None)

get the subpage urls and return a dictionary with all the data for the list of attributes. 
If no list_of_attributes given, automatically return all the attributes found.
If no data are available for a specific attribute the function will describe it as None.


In addition, the code will create a file home.log with the logging and stdout.log with the output.



## Authors

Noa Kawa Keren Portugais


