from bs4 import BeautifulSoup
import requests

PAGES = 51


def pages_to_dict(no_of_page):
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


def get_data(link_sub_page):
    """
    This function get the subpage and return a dictionary with all the data
    :param link_sub_page: link
    :return: dictionary with all all data of a sub_page
    """
    sub_page = requests.get(link_sub_page).text
    data = dict()
    soup = BeautifulSoup(sub_page, 'lxml')

    price = soup.find(class_="number")
    data['price'] = price.text.strip()

    features = soup.find('dl')  # find the first dl

    for feature in features.find_all('dt'):
        data[feature.text.strip()] = feature.findNext('dd').text.strip()

    col = soup.find(class_="col-sm-12")
    for col in col.find_all('section'):
        if col.h2.text == "Here's a brief description":
            data['description'] = col.p.text
        if col.h2.text == "Features":
            data['features'] = col.find(class_='features-checkboxes columns-3').text.split('\n')[1:-1]

    return data


def main():
    links = pages_to_dict(1)
    sub_links = get_sub_page(links[0])
    print(get_data(sub_links[0]))


if __name__ == '__main__':
    main()