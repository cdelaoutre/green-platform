from boto3.dynamodb.types import TypeSerializer

class URLBuilder:
    def __init__(self, params, current_datetime, idTable):
        self.params = params
        self.current_datetime = current_datetime
        self.idTable = idTable

    def build_shopify_url(self):
        #Get page number:
        ts = TypeSerializer()
        pageNumber = int(ts.serialize(self.params['pages'])['N'])
        query_params = [{"url" : "{}products.json?page={}".format(self.params['url'], p),
                          "country" : self.params['country'],
                          "current_datetime" : self.current_datetime,
                          "id_shop" : self.idTable
                         } for p in range(1,pageNumber+1)]
        return query_params
    
    def build_url(self):
        if self.params['type'] == 'shopify':
            return self.build_shopify_url()
