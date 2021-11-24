URL = 'https://www.ihomes.co.il/s/tel-aviv-yafo?page='
PAGES = 51
BATCHES = 10
HE_TO_EN = {'פנטהאוז': 'Penthouse', 'בית': 'House', 'דירת גן': 'Garden Apartment', 'דופלקס': 'Duplex',
            'דו משפחתי': 'Semi-detatched', 'וילה': 'Villa', "קוטג'": 'Cottage', 'מגרש': 'Plot', 'סטודיו': 'Studio',
            'משרד': 'Office', 'מיני פנטהוז': 'Mini Penthouse', 'דירה': 'Apartment', 'בנין': 'building'}
ATTRIBUTES = ['Price', 'Sale or Rent ?', 'Condition', 'Type of property', 'Floors in building', 'Floor', 'Rooms',
              'Built Area', 'Furnished', 'First listed']
CITY = 'jerusalem'
HELP_STRING = f"""
arg1: [Sell, Rent]
arg2: Maximum price
arg3: Minimum date dd/mm/yyyy
arg4: City - Choose from the following cities: [r - raanana, j - jerusalem, tlv - tel-aviv-yafo, hrtz - herzliya, ad - ashdod, bs - beer-sheva, e - eilat, 
t -tiberias, by ) bat-yam, h - haifa, n - netanya, ak - ashkelon]
"""

CITIES = {'r': 'raanana', 'j': 'jerusalem', 'tlv': 'tel-aviv-yafo', 'hrtz': 'herzliya', 'ad': 'ashdod', 'bs': 'beer-sheva', 'e': 'eilat',
        't': 'tiberias', 'by': 'bat-yam', 'h': 'haifa', 'n': 'netanya', 'ak': 'ashkelon'}

NUM_ARGS_NO_ARGS = 1
NUM_ARGS_HELP = 2
{'Link': 'https://www.ihomes.co.il/p/NTc2MA', 'Price': '₪  9,800,000', 'Sale or Rent ?': 'Sell', 'Condition': None,
 'Type of property': 'Apartment', 'Floors in building': '0', 'Floor': '0', 'Rooms': '12', 'Built Area': '220.4 m2',
 'Furnished': 'forms.No', 'First listed': '24/10/2021', 'Features': ['מרתף', 'מרפסת', 'מחסן']}
