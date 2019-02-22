import trace

class   Server():
    def __init__(self, url = 'localhost', port = 1883):
        self.url = url
        self.port = port
        self.ca_cert = None
        self.trace = trace.Trace(self)

    def set_config(self, config):
        if config is not None:
            try:
                if config.get('url') is not None:
                    self.url = config.get('url')
    
                if config.get('port') is not None:
                    self.port = int(config.get('port'))
    
                if config.get('ca_cert') is not None:
                    self.ca_cert = config.get('ca_cert')
    
                return  True
            except Exception as error:
                self.trace.error(error)
    
        return  False
    
    def to_dictionary(self):
        output = {}
        output['url'] = self.url
        output['port'] = self.port
        output['ca_cert'] = self.ca_cert

        return  output