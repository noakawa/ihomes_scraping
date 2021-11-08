import grequests
from bs4 import BeautifulSoup
import config


def pages_to_list(no_of_page):
    """
    This function receives the number of pages to scrap and returns a list with the links of the different pages
    :param no_of_page: integer
    :return: list with the links
    """
    links = []
    page = 1
    while page <= no_of_page:
        links.append(config.link+page)
        page += 1
    return links


def links_to_soup(urls, batches):
    """
    transform a list of urls to a list of soup
    :param urls: list of urls
    :param batches: size for grequests
    :return: list of soup
    """
    sub_pages = (grequests.get(u) for u in urls)
    sub_responses = grequests.map(sub_pages, size=batches)
    soup = []
    for res in sub_responses:
        soup.append(BeautifulSoup(res.text, 'html.parser'))
    return soup


def get_sub_page(urls, batches=config.BATCHES):
    """
    This function receives the links of all pages and returns a list of all subpages.
    :param batches: size for grequests
    :param urls: list of links
    :return: list with the sub links
    """
    subpages = []
    for soup_page in links_to_soup(urls, batches):
        for detail in soup_page.find_all(class_="detail text-caps underline"):
            subpages.append(detail['href'])

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
    price = soup.find(class_="number")
    all_data['Price'] = price.text.strip()

    features = soup.find('dl')  # find the first dl

    for feature in features.find_all('dt'):
        # Translating from hebrew to english
        if feature.text.strip() == 'Type of property': #TODO: try catch
            all_data[feature.text.strip()] = config.HE_TO_EN[feature.findNext('dd').text.strip()]
        else:
            all_data[feature.text.strip()] = feature.findNext('dd').text.strip()

    col = soup.find(class_="col-sm-12")
    for col in col.find_all('section'):
        if col.h2.text == "Here's a brief description":
            all_data['Description'] = col.p.text
        if col.h2.text == "Features":
            all_data['Features'] = col.find(class_='features-checkboxes columns-3').text.split('\n')[1:-1]

    if list_of_attributes is None:
        return all_data

    data = {'Link': sub_link}
    for attribute in list_of_attributes:
        if attribute in all_data:
            data[attribute] = all_data[attribute]
        else:
            data[attribute] = None
    return data


def main():
    links = pages_to_list(config.PAGES)
    sub_links = get_sub_page(links)
    for i, soup in enumerate(links_to_soup(sub_links)):
        print(get_data(soup, sub_links[i], config.ATTRIBUTES))


if __name__ == '__main__':
    main()
