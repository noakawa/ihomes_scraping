from bs4 import BeautifulSoup
import requests

headers = {'Accept-Language': 'en'}
dct = dict()
source = requests.get('https://www.ihomes.co.il/s/tel-aviv-yafo?page=1', headers=headers).text
soup = BeautifulSoup(source, 'lxml')

details = soup.find_all(class_="detail text-caps underline")
link = details[0]['href']

sub_page = requests.get(link).text
sub_soup = BeautifulSoup(sub_page, 'lxml')

price = sub_soup.find(class_="number")
dct['price'] = price.text.strip()

features = sub_soup.find('dl')  # find the first dl

for feature in features.find_all('dt'):
    dct[feature.text.strip()] = feature.findNext('dd').text.strip()

col = sub_soup.find(class_="col-sm-12")
for col in col.find_all('section'):
    if col.h2.text == "Here's a brief description":
        dct['description'] = col.p.text
    if col.h2.text == "Features":
        dct['features'] = col.find(class_='features-checkboxes columns-3').text.split('\n')[1:-1]


print(dct)

