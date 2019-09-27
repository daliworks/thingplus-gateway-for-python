import trace

class   Server():
    def __init__(self, url = 'localhost', port = 80):
        self.url = url
        self.port = port
        self.gateways = []

    def attach(self, _gateway):
        self.gateways.append(_gateway)

    def to_dictionary(self):
        output = {}
        output['url']  = self.url
        output['port'] = self.port

        return  output

    def create_client(slef):
        return  None
