from aliexpress_api_client import AliExpress
from PIL import Image, ImageChops
import urllib, cStringIO
 
import math, operator

def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*((idx%256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

def strdiff(s1, s2):
   s1 = s1.lower()
   s2 = s2.lower()
   count = 0
   l1 = s1.split(' ')
   for item in l1:
      if (s2.find(item) != -1):
         count += 1
   return count

def get_perc(mi, ma, va):
   if (mi == ma):
      for item in va:
         yield 100.0
   else:      
      for item in va:
         yield (1 - (item - mi)/(ma - mi))*100

def get_max_ind(a):
   x = max(a)
   for i in range(len(a)):
      if (a[i] == x):
         return i
      
def get_avg(f1, f2):
   return (f1 + f2) / 2.0

def price_float(s):
   return float(s[4:])

def calc_result(s_item, or_price, or_img):

   aliexpress = AliExpress('33503')

   s_item = raw_input("Enter item name: ")

   not_working = True

   products = {}
   while (not_working and s_item != ''):
      try:
         products = aliexpress.get_product_list(['productTitle', 'salePrice', 'imageUrl', 'productUrl'], s_item)['products']
         not_working = False
      except:
         s_item = ' '.join(s_item.split(' ')[:-1]).strip()
         print s_item


   print '\n\n'

   or_img_link = cStringIO.StringIO(urllib.urlopen(item['imageUrl']).read())
   orig_img = Image.open(or_img_link)
      
   titles = []
   image_diffs = []

   for item in products:
      titles.append(item['productTitle'])
      print item['productTitle'] + item['salePrice'] + '\n' + item['imageUrl'] + '\n'
      img_link = cStringIO.StringIO(urllib.urlopen(item['imageUrl']).read())
      img = Image.open(img_link)
      image_diffs.append(rmsdiff(img, orig_img))
      #a = raw_input();
      print '___________________________________________________________________________'

   string_diffs = map(strdiff, [s_item]*len(titles), titles)
   max_strdiff = float(max(string_diffs))
   max_imgdiff = float(max(image_diffs))
   min_strdiff = float(min(string_diffs))
   min_imgdiff = float(min(image_diffs))

   str_data = list(get_perc(min_strdiff, max_strdiff, string_diffs))
   img_data = list(get_perc(min_imgdiff, max_imgdiff, image_diffs))
   comp_data = map(get_avg, str_data, img_data)


   new_price = products[get_max_ind(comp_data)]['salePrice']
   if (or_price < price_float(new_price)):
      return products[get_max_ind(comp_data)]['productUrl'], -1
   else:
      return products[get_max_ind(comp_data)]['productUrl'], price_float(new_price)

