import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    def read_table(TableName):
        client = boto3.client("dynamodb")
        paginator = client.get_paginator("scan")
        page_iterator = paginator.paginate(TableName=TableName)
        res = {'data' : []}
        for page in page_iterator:
                for item in page["Items"]:
                    res['data'].append(item)
        return res
    shops = read_table("gp-shops")
    
    #Set Params
    client = boto3.client("lambda")
    currDatetime = datetime.now().strftime("%Y%m%d%H%M")
    
    for s in shops:
        for p in range(1, int(s['pages'])+1):
            inputParams = {
            "url": s['url'],
            "page": p,
            "country": s['country'],
            "datetime": currDatetime,
            "idShop" : s['idShop']
            }
            client.invoke(
                FunctionName = 'arn:aws:lambda:ap-south-1:033225783542:function:scrap_shopify',
                InvocationType = 'Event',
                Payload = json.dumps(inputParams))
    return {'status' : 'done'}
