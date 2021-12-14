import grequests
import config
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename='home.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def access_url(response, url):
    """ This function send a logging for access a url"""
    if response.status_code == 200:
        logging.info(f'{url} successfully accessed')
    else:
        logging.error(f'{url} not successfully accessed')


def url_city(city):
    """ This function return the url of the specific city """
    return f'https://www.ihomes.co.il/s/{city}'


def list_url_cities(cities):
    """
    This function return a list of urls for the cities
    :param cities: list of cities
    :return: list of urls for each city
    """

    url = []
    for city in cities:
        url.append(url_city(city))
    return url


def max_pages(city):
    """
    This function returns the maximum number of pages of link
    :param city: city to scrap
    :return: integer maximum of pages
    """
    url = url_city(city)
    page = requests.get(url)
    access_url(page, url)
    soup = BeautifulSoup(page.text, 'html.parser')
    p = soup.find(class_="page-pagination")
    try:
        pages = p.findAll(class_="page-item")
    except AttributeError:
        logging.critical("Website out of service")
        return
    return int(pages[-2].text)


def pages_to_list(city, no_of_page):
    """
    This function receives the number of pages to scrap and returns a list with the links of the different pages
    :param city: city to scrap
    :param no_of_page: integer
    :return: list with the links
    """
    links = []
    page = 1
    while page <= no_of_page:
        links.append(f'{url_city(city)}?page={page}')
        page += 1
    logging.info(f'{no_of_page} pages link in the list')
    return links


def links_to_soup(urls, batches=config.BATCHES):
    """
    transform a list of urls to a list of soup
    :param urls: list of urls
    :param batches: size for grequests
    :return: list of soup
    """
    sub_pages = (grequests.get(u) for u in urls)
    sub_responses = grequests.map(sub_pages, size=batches)
    soup = []
    for index, res in enumerate(sub_responses):
        soup.append(BeautifulSoup(res.text, 'html.parser'))
        access_url(res, urls[index])

    return soup


def get_sub_page(urls, batches=config.BATCHES):
    """
    This function receives the links of all pages and returns a list of all subpages.
    :param batches: size for grequests
    :param urls: list of links
    :return: list with the sub links
    """
    subpages = []
    for page, soup_page in enumerate(links_to_soup(urls, batches)):
        for i, detail in enumerate(soup_page.find_all(class_="detail text-caps underline")):
            try:
                subpages.append(detail['href'])
                logging.info(f'link subpage number {i + 1} for {page + 1} found')
            except AttributeError:
                logging.error(f'no href in page {page + 1}, listing number {i + 1}')

    return subpages

