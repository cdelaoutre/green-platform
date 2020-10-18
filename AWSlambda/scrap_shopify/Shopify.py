import re

class ShopifyPage():
    def __init__(self, data, params):
        self.data = data['products']
        self.params = params
        self.status = None
        self.answer = None
        self.updates_count = 0
        self.inserts_count = 0
        
    def is_empty(self):
        if self.data == []:
            self.status = 'Success'
            self.answer = {'status' : self.status,
                            'type' : 'Empty',
                           'url': self.params['url']}
            return True
        else:
            self.status = 'To be treated'
            return False
            
    def increment_updates(self, i):
        self.updates_count += 1
        
    def increment_inserts(self, i):
        self.inserts_count += 1
        
    def set_answer(self):
        self.answer = {'status' : 'Success',
                                'type' : 'Scrapped',
                                'url': self.params['url'],
                                'updates_count' : self.updates_count,
                                'inserts_count' : self.inserts_count,
            }
        return self.answer
    
    
class ShopifyProduct():
    def __init__(self, data, params):
        self.data = data
        self.params = params

    def prepare_data(self):
        #Remove HTML
        self.data['body_html'] = re.sub('<.*?>', '', self.data['body_html'])
        #Rename body_html
        def changeKey(k):
            ck = {'body_html':'description'}
            if k in ck.keys():
                return ck[k]
            else: return k
        self.data = {changeKey(k): v for k, v in self.data.items()}
        #Adding additional values
        self.data['idProduct'] = '{}_{}_{}'.format(self.params['country'], self.params['id_shop'], self.data['id'])
        self.data['type'] = 'shopify'
        self.data['idShop'] = self.params['id_shop']
        self.data['lastUpdate'] = self.params['current_datetime']
        return 'Treated'
        
    def is_different_from(self, new_item):
        exclude = ['lastUpdate']
        new_item = {k : v for k,v in new_item.items() if k not in exclude}
        prev_item = {k : v for k,v in self.data.items() if k not in exclude}
        if new_item != prev_item:
            return True
        else :
            return False