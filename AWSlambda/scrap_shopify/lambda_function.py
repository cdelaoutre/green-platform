from RequestURL import RequestURL
from Shopify import ShopifyPage, ShopifyProduct
from DynamoQuery import DynamoQuery

import boto3

def lambda_handler(event, context):
    params = event #Must include : url, country, current_datetime, id_shop

    #Setting dynamo
    dynamo_products = DynamoQuery('gp-products')
    
    #Make Request
    req = RequestURL(params)
    req.try_request()
    if req.status == 'Failed':
        return req.answer
    
    #Check for empty page
    shopify_page = ShopifyPage(req.answer, params)
    if shopify_page.is_empty():
        return shopify_page.answer
    
    #Treat Data
    for element in shopify_page.data:
        shopify_product = ShopifyProduct(element, params)
        shopify_product.prepare_data()
    
        #Write Data
        current_id = shopify_product.data['idProduct']
        matching_item = dynamo_products.get_item_from_id(current_id)
    
        if matching_item is None: 
            #Insert Product
            dynamo_products.put_item(shopify_product.data)
            shopify_page.increment_inserts(1)
    
        elif shopify_product.is_different_from(matching_item):
            #Update Product
            dynamo_products.put_item(shopify_product.data)
            shopify_page.increment_updates(1)
        else:
            #No need to Insert/Update
            pass
    
    res = shopify_page.set_answer()
    return res