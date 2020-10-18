from URLBuilder import URLBuilder
from DynamoQuery import DynamoQuery

import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    
    #Set Params
    client = boto3.client('lambda')
    current_datetime = datetime.now().strftime("%Y%m%d%H%M")

    #Get all shops
    shops = DynamoQuery('gp-shops').get_all_table()
    
    #Query shops
    shops_count, queries_count = (0,0)
    for shop in shops:
        
        queries_params = URLBuilder(shop, current_datetime, 'idShop').build_url()
        
        shops_count +=1
        for query_params in queries_params:
            client.invoke(
                FunctionName = 'scrap_{}'.format(shop['type']),
                InvocationType = 'Event',
                Payload = json.dumps(query_params))
            queries_count +=1
    
    res = {'status':'Succesful',
            'nbShops' : shops_count,
            'nbQueries' : queries_count}
    return res
