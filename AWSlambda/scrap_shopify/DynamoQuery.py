import boto3

class DynamoQuery:
    def __init__(self, table):
        self.table = table
        self.tables_keys = {'gp-products':'idProduct', 'gp-shops':'idShop'}
        self.query_base = boto3.resource('dynamodb').Table(table)

    def get_item_from_id(self, id):
        my_item = self.query_base.get_item(Key={self.tables_keys[self.table]: id})
        if "Item" not in my_item.keys():
            return None
        else:
            return my_item["Item"]
            
    def put_item(self, element):
        self.query_base.put_item(Item=element)
