import config
from datetime import datetime
import re
from currency_converter import CurrencyConverter
import argparse
import out_of_scrap
import logging

logging.basicConfig(filename='home.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def get_data(city, soup, sub_link, sell_or_rent=False, max_price=False, min_date=False):
    """
    This function get the subpage and return a dictionary with all the all_data for the list of attributes
    :param city: city of the data
    :param soup: link converted to soup
    :param sub_link: link
    :param sell_or_rent: False if we take sell and rent, value otherwise
    :param max_price: maximum price to list
    :param min_date: minimum date when listed
    :return: dictionary with all all all_data of a sub_page
    """

    all_data = {'Link': sub_link, 'City': city}
    try:
        features = soup.find('dl')  # find the first dl
        all_data = get_features(all_data, features, sub_link)
        if min_date and all_data['First listed'] < min_date:
            return
        if sell_or_rent and all_data['Sale or Rent ?'].lower() != sell_or_rent:
            return
        all_data = get_price(soup, all_data, sub_link)
        if max_price and all_data['Price'] > max_price:
            return
    except AttributeError:
        logging.error(f'{sub_link}: additional features including description not found')

    # Replacing empty string by None
    all_data_n = {k: None if not v else v for k, v in all_data.items()}
    data = subset_data(all_data_n, config.ATTRIBUTES, sub_link, city)
    return data


def price_shekels(price):
    """
    This function returns the price in shekels if it is not
    :param price: price
    :return: price in shekels
    """
    try:
        num = int(''.join(re.findall('[0-9]+', price)))
    except ValueError:
        return
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
        elif feature.text.strip() == 'Built Area':
            try:
                all_data[feature.text.strip()] = \
                    int(''.join(re.findall('[0-9]+', feature.findNext('dd').text.strip()))[0:-1])
            except ValueError:
                all_data[feature.text.strip()] = None
        else:
            try:
                all_data[feature.text.strip()] = int(feature.findNext('dd').text.strip())
                logging.info(f'{sub_link}: {feature.text.strip()} found (integer)')
            except ValueError:
                all_data[feature.text.strip()] = feature.findNext('dd').text.strip()
                logging.info(f'{sub_link}: {feature.text.strip()} found (not integer)')
    return all_data


def subset_data(all_data_n, list_of_attributes, sub_link, city):
    """
    This function returns a dictionary with the specific data asked
    :param city: city to scrap
    :param all_data_n: all the data that was scraped
    :param list_of_attributes: attributes needed
    :param sub_link: link of the house
    :return: Dictionary with new data
    """
    data = {'Link': sub_link, 'City': city}
    for attribute in list_of_attributes:
        if attribute in all_data_n:
            data[attribute] = all_data_n[attribute]
        else:
            data[attribute] = None
            logging.info(f'{sub_link}: REQUIRED {attribute} not found')
    return data


def valid_date(s):
    """ This function raise an error if the format of the input date is not correct """
    try:
        return datetime.strptime(s, "%d/%m/%Y")
    except Exception:
        msg = "not a valid date: {0!r}\nGood format: DD/MM/YYYY".format(s)
        raise argparse.ArgumentTypeError(msg)


def print_output(s, p, d, city):
    city_to_slinks = dict()
    values = []
    if not city:
        for c in config.CITIES.values():
            links = out_of_scrap.pages_to_list(c, out_of_scrap.max_pages(c))
            city_to_slinks[c] = out_of_scrap.get_sub_page(links)
    else:
        links = out_of_scrap.pages_to_list(config.CITIES[city], out_of_scrap.max_pages(config.CITIES[city]))
        city_to_slinks[config.CITIES[city]] = out_of_scrap.get_sub_page(links)

    for city in city_to_slinks:
        for i, soup in enumerate(out_of_scrap.links_to_soup(city_to_slinks[city])):
            value = get_data(city, soup, city_to_slinks[city][i],
                             sell_or_rent=s, max_price=p, min_date=d)
            # print(value)
            values.append(value)
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sale_or_rent', help=f"choose from ({','.join(config.OPTIONS)})",
                        choices=config.OPTIONS, default=False)
    parser.add_argument('-p', '--max_price', type=float, help='maximum price for each house', default=False)
    parser.add_argument('-d', '--min_date', help='minimum date it was listed - format DD/MM/YYYY',
                        type=valid_date, default=False)
    parser.add_argument('-c', '--cities', help=f"choose from the keys : {config.CITIES}", choices=config.CITIES.keys(),
                        default=False)
    args = parser.parse_args()
    s = args.sale_or_rent
    price = args.max_price
    date = args.min_date
    city = args.cities

    return print_output(s, price, date, city)


if __name__ == '__main__':
    main()
