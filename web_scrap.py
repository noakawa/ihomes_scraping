from bs4 import BeautifulSoup
import requests

PAGES = 51


def pages_to_list(no_of_page):
    """
    This function receives the number of pages to scrap and returns a list with the links of the different pages
    :param no_of_page: integer
    :return: list with the links
    """
    links = []
    page = 1
    while page <= no_of_page:
        links.append(f'https://www.ihomes.co.il/s/tel-aviv-yafo?page={page}')
        page += 1
    return links


def get_sub_page(link_page):
    """
    This function receives the link of a page and returns a list of all subpages.
    :param link_page: link
    :return: list with the sub links
    """
    headers = {'Accept-Language': 'en'}
    source = requests.get(link_page, headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    subpages = []
    for detail in soup.find_all(class_="detail text-caps underline"):
        subpages.append(detail['href'])
    return subpages


def get_data(link_sub_page, list_of_attributes=None):
    """
    This function get the subpage and return a dictionary with all the all_data for the list of attributes
    :param list_of_attributes: list of attributes needed
    :param link_sub_page: link
    :return: dictionary with all all all_data of a sub_page
    """
    sub_page = requests.get(link_sub_page).text
    all_data = {'Link': link_sub_page}
    soup = BeautifulSoup(sub_page, 'lxml')

    price = soup.find(class_="number")
    all_data['Price'] = price.text.strip()

    features = soup.find('dl')  # find the first dl

    for feature in features.find_all('dt'):
        all_data[feature.text.strip()] = feature.findNext('dd').text.strip()

    col = soup.find(class_="col-sm-12")
    for col in col.find_all('section'):
        if col.h2.text == "Here's a brief description":
            all_data['Description'] = col.p.text
        if col.h2.text == "Features":
            all_data['Features'] = col.find(class_='features-checkboxes columns-3').text.split('\n')[1:-1]

    if list_of_attributes is None:
        return all_data

    data = {'Link': link_sub_page}
    for attribute in list_of_attributes:
        data[attribute] = all_data[attribute]
    return data


def main():
    links = pages_to_list(1)
    sub_links = get_sub_page(links[0])
    attributes = ['Price', 'Sale or Rent ?', 'Condition', 'Type of property', 'Floors in building', 'Floor', 'Rooms']
    print(get_data(sub_links[0], attributes))


if __name__ == '__main__':
    main()
