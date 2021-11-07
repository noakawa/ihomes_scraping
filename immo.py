import requests

links = []
page = 1
while page <= 51:
    links.append(f'https://www.ihomes.co.il/s/tel-aviv-yafo?page={page}')
    page += 1

for page, link in enumerate(links):
    with open('/Users/Kawa/Documents/ITC/PythonRequests/page'+str(page)+'.txt', 'w') as dst:
        req = requests.get(link)
        req.encoding = 'ISO-8859-1'
        dst.write(str(req.text))

#headers
#cookies.get_dict()


