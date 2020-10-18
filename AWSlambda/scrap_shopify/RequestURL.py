import urllib.request
import json

class RequestURL:
    def __init__(self, params):
        self.params = params
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        self.answer = None
        self.status = 'Non made'
    def try_request(self):
        req = urllib.request.Request(self.params['url'],
                                    data=None,
                                    headers={'User-Agent': self.user_agent}
                                    )
        try:
            data = urllib.request.urlopen(req).read()
            data = json.loads(data)
            self.answer = data
            self.status = 'Success'
        except :
            self.status = 'Failed'
            self.answer = {'status' : self.status,
                           'error' : 'HTTP request failed',
                           'url': self.params['url']}
        return self.status