# Data mining iHomes

Gather data from iHomes, Israel's real estates online listing.  

## Getting Started

This project contains 4 files: config.py, requirements.txt, web_scrap.py and README.md

There are implemented to scrap data from iHomes website
and gather information about properties in Tel Aviv only 

It is implemented using bs4 and grequests (see ### Prerequisites)

### Prerequisites

What things you need to install the software and how to install them

1. Install pip:
If pip is not installed already (you can check it using – “pip –version” in your command or shell prompt), 
you can install by giving below command:
-For Linux environment
```
$sudo apt-get install python-pip
```
-For Window environment
```
>python get-pip.py
```

2. Python library gRequests 
    You can make use of pip, easy_install, or tarball
    To see the full list of options at your disposal, you can view the official install 
    documentation for Requests here: [http://docs.python-requests.org/en/latest/user/install/]()

Example: use pip to install the library
In your Python interpreter, type the following:
```
pip install grequests
```
3. BeautifulSoup library 
a. First create a virtual environment (optional) - it will allow you to create an isolated working copy of python for a specific project without affecting the outside setup
    Then, as BeautifulSoup is not a standard library, we need to install it, 
for example using pip:
```
pip install beautifulsoup4
```
See the link below for a full list of option: 
https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_installation.htm

b. Installing BeautifulSoup
For Linux machine:
To install bs4 on Debian or Ubuntu linux using system package manager, run the below command −
```
$sudo apt-get install python-bs4 (for python 2.x)
$sudo apt-get install python3-bs4 (for python 3.x)
```
using easy_install or pip:
```
$easy_install beautifulsoup4
$pip install beautifulsoup4
```
On Window machine:
```
>pip install beautifulsoup4
```
4. Installing a parser
On Linux Machine:
```
$apt-get install python-lxml
$apt-get insall python-html5lib
```
Windows Machine:
```
$pip install lxml
$pip install html5lib
```
### Installing

After installing the required library (explained in ### Prerequisites)
Downloads the four files and run web_scrap.py.


### Implementation

1. confy.py is a configuration file that has five variable:
```
URL = 'https://www.ihomes.co.il/s/tel-aviv-yafo?page='
```
the url of iHomes website 

PAGE: the number of web pages from which we'll gather data in this case 51
'https://www.ihomes.co.il/s/tel-aviv-yafo?page=XX' in the previous url we will replace XX 
with the page number 1-51

BATCHES : the number of batches used for the grequest
HE_TO_EN: A dictionary used to translate words from hebrew to english. 
iHomes is originally an israeli website implemented in hebrew with available english translation, 
scraping data using grequest and bs4 do not automatically translate the data, 
therefore we created HE_TO_EN to make the translation

Those variables are called in web_scrap.py and referenced as:
```
config.[VARIABLE_NAME]
```

2. web_scrap.py contain a python code which calls main() and three other functions

pages_to_list(no_of_page) return a list of links of pages in the website depending on the input number 
in our case number of pages is 51, defined in the config file.
links_to_soup(urls, batches=config.BATCHES): will create a soup object using for each input urls, using grequest and the input batches number
get_data(soup, sub_link, list_of_attributes=None): get the subpage urls and return a dictionary with all the data for the list of attributes (defines in config.py)
If no data are available for a specific attribute the function will describe it as None

In addition, the code will create a file home.log with the logging.


3. requirement.txt: 



## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors
Noa Kawa
Keren Portugais


