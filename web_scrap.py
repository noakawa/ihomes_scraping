import grequests
from bs4 import BeautifulSoup
import config
import sys
import logging

sys.stdout = open('stdout.log', 'w')
logging.basicConfig(filename='home.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def pages_to_list(no_of_page):
    """
    This function receives the number of pages to scrap and returns a list with the links of the different pages
    :param no_of_page: integer
    :return: list with the links
    """
    links = []
    page = 1
    while page <= no_of_page:
        links.append(f'{config.URL}{page}')
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


def get_data(soup, sub_link, list_of_attributes=None):
    """
    This function get the subpage and return a dictionary with all the all_data for the list of attributes
    :param list_of_attributes: list of attributes needed
    :param soup: link converted to soup
    :param sub_link: link
    :return: dictionary with all all all_data of a sub_page
    """

    all_data = {'Link': sub_link}
    all_data = get_price(soup, all_data, sub_link)
    features = soup.find('dl')  # find the first dl
    all_data = get_features(all_data, features, sub_link)
    try:
        col = soup.find(class_="col-sm-12")
    except AttributeError:
        logging.error(f'{sub_link}: additional features including description not found')
    all_data = get_sections(all_data, col, sub_link)

    # Replacing empty string by None
    all_data_n = {k: None if not v else v for k, v in all_data.items()}
    if list_of_attributes is None:
        return all_data_n
    else:
        return subset_data(all_data_n, list_of_attributes, sub_link)


def get_price(soup, all_data, sub_link):
    price = soup.find(class_="number")
    try:
        all_data['Price'] = price.text.strip()
        logging.info(f'{sub_link}: price found')
    except AttributeError:
        logging.error(f'{sub_link}: no price found')
    return all_data


def get_features(all_data, features, sub_link):
    for feature in features.find_all('dt'):
        # Translating from hebrew to english
        if feature.text.strip() == 'Type of property':
            try:
                all_data[feature.text.strip()] = config.HE_TO_EN[feature.findNext('dd').text.strip()]
            except KeyError:
                logging.error(f'{sub_link}: no translation for {feature.findNext("dd").text.strip()}')
                all_data[feature.text.strip()] = feature.findNext('dd').text.strip()
        else:
            all_data[feature.text.strip()] = feature.findNext('dd').text.strip()
            logging.info(f'{sub_link}: {feature.text.strip()} found')
    return all_data


def get_sections(all_data, col, sub_link):
    for col in col.find_all('section'):
        if col.h2.text == "Here's a brief description":
            try:
                all_data['Description'] = col.p.text
            except AttributeError:
                logging.error(f'{sub_link}: description not found')
        if col.h2.text == "Features":
            try:
                all_data['Features'] = col.find(class_='features-checkboxes columns-3').text.split('\n')[1:-1]
            except AttributeError:
                logging.error(f'{sub_link}: additional features not found')
    return all_data


def subset_data(all_data_n, list_of_attributes, sub_link):
    data = {'Link': sub_link}
    for attribute in list_of_attributes:
        if attribute in all_data_n:
            data[attribute] = all_data_n[attribute]
        else:
            data[attribute] = None
            logging.info(f'{sub_link}: REQUIRED {attribute} not found')
    return data

def main():
    links = pages_to_list()
    sub_links = get_sub_page(links)
    count = 0
    for i, soup in enumerate(links_to_soup(sub_links)):
        print(get_data(soup, sub_links[i], '01/10/2021'))
        count += 1
    print(count)

if __name__ == '__main__':
    main()
