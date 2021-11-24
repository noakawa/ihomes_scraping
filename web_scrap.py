import grequests
from bs4 import BeautifulSoup
import config
import logging
import requests
from datetime import datetime
import re
from currency_converter import CurrencyConverter
import argparse

logging.basicConfig(filename='home.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def url_city(city):
    """ This function return the url od the specific city """
    return f'https://www.ihomes.co.il/s/{city}'


def max_pages(city):
    """
    This function returns the maximum number of pages of link
    :param city: city to scrap
    :return: integer maximum of pages
    """
    url = url_city(city)
    page = requests.get(url)
    if page.status_code == 200:
        logging.info(f'{url} successfully accessed')
    else:
        logging.error(f'{url} not successfully accessed')
    soup = BeautifulSoup(page.text, 'html.parser')
    p = soup.find(class_="page-pagination")
    pages = p.findAll(class_="page-item")
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
        if res.status_code == 200:
            logging.info(f'{urls[index]} successfully accessed')
        else:
            logging.error(f'{urls[index]} not successfully accessed')

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


def get_data(soup, sub_link, max_price=None, min_date=None, list_of_attributes=None, sell=True, rent=True):
    """
    This function get the subpage and return a dictionary with all the all_data for the list of attributes
    :param max_price: maximum price to list
    :param rent: Show only the ones to rent
    :param sell: Show only the ones to sale
    :param list_of_attributes: list of attributes needed
    :param soup: link converted to soup
    :param sub_link: link
    :param min_date: minimum date when listed
    :return: dictionary with all all all_data of a sub_page
    """

    all_data = {'Link': sub_link}
    try:
        features = soup.find('dl')  # find the first dl
        all_data = get_features(all_data, features, sub_link)
        if min_date is not None and all_data['First listed'] < datetime.strptime(min_date, "%d/%m/%Y"):
            return
        if (all_data['Sale or Rent ?'] == 'Sell' and sell is False) or \
                (all_data['Sale or Rent ?'] == 'Rent' and rent is False):
            return
        all_data = get_price(soup, all_data, sub_link)
        if max_price is not None and all_data['Price'] > max_price:
            return
        col = soup.find(class_="col-sm-12")
        all_data = get_sections(all_data, col, sub_link)
    except AttributeError:
        logging.error(f'{sub_link}: additional features including description not found')

    # Replacing empty string by None
    all_data_n = {k: None if not v else v for k, v in all_data.items()}
    if list_of_attributes is None:
        return all_data_n
    else:
        return subset_data(all_data_n, list_of_attributes, sub_link)


def price_shekels(price):
    """
    This function returns the price in shekels if it is not
    :param price: price
    :return: price in shekels
    """
    num = int(''.join(re.findall('[0-9]+', price)))
    c = CurrencyConverter()
    if price[0] == '$':
        return int(c.convert(num, 'USD', 'ILS'))
    else:
        return int(num)


def get_price(soup, all_data, sub_link):
    """
    This function returns the dictionary updated with the price
    :param soup: link converted to soup
    :param all_data: previous dictionary
    :param sub_link: link of the house
    :return: all_data updated
    """
    price = soup.find(class_="number")
    try:
        all_data['Price'] = price_shekels(price.text.strip())
        logging.info(f'{sub_link}: price found')
    except AttributeError:
        logging.error(f'{sub_link}: no price found')
    return all_data


def get_features(all_data, features, sub_link):
    """
    This function returns the dictionary updated with the features
    :param all_data: previous dictionary
    :param features: list of features as html text
    :param sub_link: link of the house
    :return: all_data updated
    """
    for feature in features.find_all('dt'):
        # Translating from hebrew to english
        if feature.text.strip() == 'Type of property':
            try:
                all_data[feature.text.strip()] = config.HE_TO_EN[feature.findNext('dd').text.strip()]
            except KeyError:
                logging.error(f'{sub_link}: no translation for {feature.findNext("dd").text.strip()}')
                all_data[feature.text.strip()] = feature.findNext('dd').text.strip()
        elif feature.text.strip() == 'First listed':
            all_data['First listed'] = datetime.strptime(feature.findNext('dd').text.strip(), "%d/%m/%Y")
        else:
            all_data[feature.text.strip()] = feature.findNext('dd').text.strip()
            logging.info(f'{sub_link}: {feature.text.strip()} found')
    return all_data


def get_sections(all_data, col, sub_link):
    """
    This function returns the dictionary updated with the features in the bottom part of the page
    :param all_data: previous dictionary
    :param col: list of features as html text
    :param sub_link: link of the house
    :return: all_data updated
    """
    for col in col.find_all('section'):
        if col.h2.text == "Features":
            try:
                all_data['Features'] = col.find(class_='features-checkboxes columns-3').text.split('\n')[1:-1]
            except AttributeError:
                logging.error(f'{sub_link}: additional features not found')
    return all_data


def subset_data(all_data_n, list_of_attributes, sub_link):
    """
    This function returns a dictionary with the specific data asked
    :param all_data_n: all the data that was scraped
    :param list_of_attributes: attributes needed
    :param sub_link: link of the house
    :return: Dictionary with new data
    """
    data = {'Link': sub_link}
    for attribute in list_of_attributes:
        if attribute in all_data_n:
            data[attribute] = all_data_n[attribute]
        else:
            data[attribute] = None
            logging.info(f'{sub_link}: REQUIRED {attribute} not found')
    return data


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sale_or_rent', help=f"choose from ({','.join(config.OPTIONS)})",
                        choices=config.OPTIONS, default=True)
    parser.add_argument('-p', '--max_price', type=float, help='maximum price for each house', default=True)
    parser.add_argument('-d', '--min_date', help='minimum date it was listed - format DD/MM/YYYY',
                        type=valid_date, default=True)
    parser.add_argument('-c', '--cities', help=f"choose from the keys : {config.CITIES}", choices=config.CITIES.keys(),
                        default=True)
    args = parser.parse_args()
    s = args.sale_or_rent
    price = args.max_price
    date = args.min_date
    city = args.cities

    if s and price and date and city:
        links = pages_to_list(config.CITY, max_pages(config.CITY))
        sub_links = get_sub_page(links)
        for i, soup in enumerate(links_to_soup(sub_links)):
            print(get_data(soup, sub_links[i], list_of_attributes=config.ATTRIBUTES))

    else:
        links = pages_to_list(config.CITIES[city], max_pages(config.CITIES[city]))
        sub_links = get_sub_page(links)
    print(s)

    #     for i, soup in enumerate(links_to_soup(sub_links)):
    #         data = get_data(soup, sub_links[i], config.ATTRIBUTES)
    #         if data['S']
    #         sell = True
    #         rent = True
    #         if sys.argv[1] == 'Sell':
    #             rent = False
    #         if sys.argv[1] == 'Rent':
    #             sell = False
    #         print(get_data(soup, sub_links[i], sys.argv[2], sys.argv[3], sell=sell, rent=rent))
    #         count += 1
    #     print(count)


if __name__ == '__main__':
    main()
