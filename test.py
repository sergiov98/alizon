import configparser
from amazon.api import AmazonAPI
from aliexp import calc_result
import sys

def main():

  config = configparser.ConfigParser()
  config.read('config.ini')

  AMAZON_KEY = config.get('amazon', 'AMAZON_KEY')
  AMAZON_SECRET = config.get('amazon', 'AMAZON_SECRET')
  AMAZON_ASSOCIATE = config.get('amazon', 'AMAZON_ASSOCIATE')
  amazon = AmazonAPI(AMAZON_KEY, AMAZON_SECRET, AMAZON_ASSOCIATE)

  print "Enter product link: "
  selfStr = argv[1]

  if ('/dp/' in selfStr) or ('/gp/' in selfStr):
    try:
      print 'Finding item...'
      product = amazon.lookup(ItemId=get_asin(selfStr))
      print 'Found item!'
      title = product.title
      price = max(product.price_and_currency[0], product.list_price[0])
      image = product.large_image_url
      print title
      print price
      print image

      link, p = calc_result(title, price, image)

      print(link + ' ' + str( p))
    except:
      print 'ERROR: PRODUCT NOT FOUND'
  else:
    print('ERROR: NOT AMAZON PRODUCT LINK')

def get_asin(text):
  '''Return Amazon ASIN'''

  if '/dp/' in text:
    start_index = text.find('/dp/') + 4
  elif '/gp/product/' in text:
    start_index = text.find('/gp/') + 12
  elif '/gp/' in text:
    start_index = text.find('/gp/') + 9
  else:
    raise ValueError('ERROR: ASIN NOT FOUND')

  if start_index + 10 > len(text):
    raise ValueError('ERROR: ASIN OUT OF RANGE')
  else:
    asin = text[start_index:start_index+10]
  return asin

if __name__ == '__main__':
  main()
