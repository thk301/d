from django.shortcuts import render, HttpResponse
from lxml import html
import requests
#import re
#import pandas as pd
import urllib2, json
import simplejson

# Create your views here.

#def index(request):
#    return HttpResponse('Hello World!')

def index(request):
    parsedData = []
    parsedData2 =[]
    if request.method == 'POST':
        restaurantname = request.POST.get('restaurant')
        req = requests.get(restaurantname)
        tree = html.fromstring(req.text)
        name_finder = tree.xpath('//div[@class="u-space-t1"]/h1[@class="biz-page-title embossed-text-white shortenough"]/text()')
        try:
            name_finder =  str(name_finder[0]).strip()
            name_finder = str(name_finder).encode('ascii', 'ignore')    #Due to encoding, "'" might throw an error
        except:
            pass
        street_finder = tree.xpath('//span[@itemprop="streetAddress"]/text()')
        city_finder = tree.xpath('//span[@itemprop="addressLocality"]/text()')
        price_finder = tree.xpath('//span[@class="bullet-after"]/span[@class="business-attribute price-range"]/text()')
        phone_finder = tree.xpath('//span[@itemprop="telephone"]/text()')
        phone_finder =  str(phone_finder[0]).strip()
        phone_lookup = phone_finder.replace(" ","").replace("-","").replace('(',"").replace(")","")
        web_finder = tree.xpath('//span[@class="biz-website js-add-url-tagging"]/a[@href]/text()')
       
        restaurantData={}
        restaurantData['name'] = name_finder
        restaurantData['addy'] = street_finder
        restaurantData['city'] = city_finder
        restaurantData['phone'] = price_finder
        restaurantData['web'] = web_finder
        
        #ratingData={}
        #pd.options.display.max_colwidth = 1000
        #ratingList = pd.read_json('https://data.cityofnewyork.us/resource/xx67-kt59.json?PHONE=2125541515', dtype='unicode').dropna()
        #ratingList = ratingList.sort_index(by=["inspection_date"], ascending=False)
        #ratingList.index =  xrange(len(ratingList))       #reindex because of removed rows
        #ratingData['date'] = ratingList['inspection_date']
        #ratingData['violation'] = ratingList['violation_description']
        url = 'https://data.cityofnewyork.us/resource/xx67-kt59.json?PHONE='+phone_lookup
        respo   = urllib2.urlopen(url)
        parsedData2 =simplejson.load(respo)
        
        #parsedData2 = json.dumps(parsedData2) 
        
        parsedData.append(restaurantData)
       
        
    return render(request, 'app/profile.html', {'data':parsedData, 'data2':parsedData2})