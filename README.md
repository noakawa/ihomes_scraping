# Data mining iHomes

Gather data from iHomes, Israel's real estates online listing.  

## Getting Started

In this project we gather data from the iHomes website url: 
https://www.ihomes.co.il/s/tel-aviv-yafo?page=XX
and go over 51 pages by replacing XX with the page number.

We collect data about the properties in Tel Aviv and return 
'Price', 'Sale or Rent ?', 'Condition', 'Type of property', 'Floors in building', 'Floor', 'Rooms'


### Prerequisites

What things you need to install the software and how to install them

1. Instal pip
	Best way to install any python package machine is using pip, however, if pip is not installed already (you can check it using – “pip –version” in your command or shell prompt), you can install by giving below command


2. Python libary Requests 
	You can make use of pip, easy_install, or tarball
	To see the full list of options at your disposal, you can view the official install 
	documentation for Requests here: http://docs.python-requests.org/en/latest/user/install/

Exemple: use pip to install the library
In your Python interpreter, type the following:
```
pip install requests
```
3. BeautifulSoup library 
	First create a virtual environment (optional) - it will allow you to create an isolated working copy of python for a specific project without affecting the outside setup
	Then, as BeautifulSoup is not a standard library, we need to install it, for exemple using pip

```
pip install beautifulsoup4
```
	See the link below for a full list of option: 
	https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_installation.htm

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

