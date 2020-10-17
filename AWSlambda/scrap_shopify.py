import json
import time
import os
import urllib.request
from urllib.error import HTTPError
import re
import boto3

def lambda_handler(event, context):
        
    #Set Params
    url = event['url']
    idShop = event['idShop']
    page = event['page']
    country = event['country']
    currDatetime = event['datetime']
    #Set DB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('gp-products')
    
    def reqURL(url, page):
        '''
        Query Shopify API
        '''
        full_url = os.path.join(url, 'products.json')
        USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        req = urllib.request.Request(full_url + '?page={}'.format(page),
                                    data=None,
                                    headers={'User-Agent': USER_AGENT}
                                    )
        try:
            data = urllib.request.urlopen(req).read()
            data = json.loads(data)
            return data
        except :
            print('ReqError : {}, page {}'.format(full_url, page))
            return {'status' : 'ReqError', 'url' : url, 'page' : page}
    
    def prepareData(p, url, country, currDatetime, idShop):
        '''
        Format one product
        '''
        #Remove HTML
        p['body_html'] = re.sub('<.*?>', '', p['body_html'])
        #Rename body_html
        def changeKey(k):
            ck = {'body_html':'description'}
            if k in ck.keys():
                return ck[k]
            else: return k
        p = {changeKey(k): v for k, v in p.items()}
        #Adding additional values
        p['idProduct'] = '{}_{}_{}'.format(country, url.split('.')[1], p['id'])
        p['country'] = country
        p['type'] = 'shopify'
        p['idShop'] = idShop
        p['lastUpdate'] = currDatetime
        return p
        
    def itemsAreDifferent(new, prev):
        exclude = ['lastUpdate']
        new = {k : v for k,v in new.items() if k not in exclude}
        prev = {k : v for k,v in prev.items() if k not in exclude}
        if new != prev:
            return True
        else :
            return False
    
    #Get Data
    
    data = reqURL(url, page)
    if 'status' in data.keys(): 
        return data
    elif data['products'] == [] :
        return {'status' : 'Empty', 'url' : url, 'page' : page}
    else :
        #Work with data
        i, u = (0,0)
        for p in data['products']:
            p = prepareData(p, url, country, currDatetime, idShop)
            readDB = table.get_item(Key={'idProduct': p['idProduct']})
            if "Item" not in readDB.keys():
                #Put the prepared item
                table.put_item(Item=p)
                i+=1

            elif itemsAreDifferent(p, readDB["Item"]):
                #Put the prepared item
                table.put_item(Item=p)
                u+=1
            else:
                #Do nothing
                pass
            
        status = {'status' : 'Succesful', 
        'nbProducts' : len(data['products']),
        'nbNewInserts' : i,
        'nbUpdates' : u,
        'url' : url,
        'page' : page
        }
        
        return status

