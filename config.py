URL = 'https://www.ihomes.co.il/s/tel-aviv-yafo?page='
BATCHES = 10
HE_TO_EN = {'פנטהאוז': 'Penthouse', 'בית': 'House', 'דירת גן': 'Garden Apartment', 'דופלקס': 'Duplex',
            'דו משפחתי': 'Semi-detatched', 'וילה': 'Villa', "קוטג'": 'Cottage', 'מגרש': 'Plot', 'סטודיו': 'Studio',
            'משרד': 'Office', 'מיני פנטהוז': 'Mini Penthouse', 'דירה': 'Apartment', 'בנין': 'building', 'חנות': 'Shop'}
ATTRIBUTES = ['Price', 'Sale or Rent ?', 'Condition', 'Type of property', 'Floors in building', 'Floor', 'Rooms',
              'Built Area', 'Furnished', 'First listed', 'Latitude', 'Longitude', 'Number_of_restaurant']
OPTIONS = ['sell', 'rent']
CITIES = {'r': 'raanana', 'tlv': 'tel-aviv-yafo', 'hrtz': 'herzliya', 'ad': 'ashdod',
          'h': 'haifa', 'n': 'netanya', 'ak': 'ashkelon'}
RADIUS = 500
API = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}%2C{}&radius={}&type=restaurant&key={}"


