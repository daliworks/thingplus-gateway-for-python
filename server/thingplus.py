import trace
import server.base
import common.gateway
import threading
import paho.mqtt.client as mqtt

class   Server(server.base.Server):
    def __init__(self, _config):
        super().__init__()
        self.ca_cert = None

        self.set_config(_config)
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
        output = super().to_dictionary()
        output['ca_cert'] = self.ca_cert

        return  output

    def create_gateway(self, config):
        config['server'] = self.to_dictionary()

        return  common.gateway.Gateway(config) 

    def create_client(self, _config, _parent):
        _config['server'] = {}
        _config['server']['url'] = self.url
        _config['server']['port'] = self.port
        _config['server']['ca_cert'] = self.ca_cert
        return  Client(_config, _parent)

class   Client(threading.Thread):
    def __init__(self, config = None, parent = None):
        threading.Thread.__init__(self)

        self.parent = parent
        self.id = None 
        self.server = {
            'url' : 'localhost',
            'port': 80,
            'ca_cert' : ''
        }
        self.keep_alive = 60
        self.qos = 0
        self.secure_mode = False
        self.user_id = None
        self.user_pw = None
        self.connected = False
        self.on_connect = None
        self.on_disconnect = None
        self.on_message = None
        self.on_publish = None
        self.trace = trace.Trace(self)
        self.trace.name = 'CL'

        self.set_config(config)

        self.mqtt_client = mqtt.Client(client_id = self.id, userdata = self)

        self.mqtt_client.on_connect = Client.mqtt_client_on_connect
        self.mqtt_client.on_disconnect = Client.mqtt_client_on_disconnect
        self.mqtt_client.on_message = Client.mqtt_client_on_message
        self.mqtt_client.on_publish = Client.mqtt_client_on_publish
        self.mqtt_client.on_log = Client.mqtt_client_on_log

    def set_config(self, config):
        if config is not None:
            try:
                if config.get('server') is not None:
                    self.server.update(config.get('server'))
    
                if config.get('id') is not None:
                    self.id = config.get('id')
    
                if config.get('keep_alive') is not None:
                    self.keep_alive = config.get('keep_aplive')
    
                if config.get('qos') is not None:
                    self.qos = config.get('qos')
    
                if config.get('user_id') is not None:
                    self.user_id = config.get('user_id')
    
                if config.get('user_pw') is not None:
                    self.user_pw = config.get('user_pw')
    
                return  True
            except Exception as error:
                self.error(error)

        return  False

    def is_connected(self):
        return  self.connected

    def subscribe(self, topic):
        self.trace.debug('Sub :', topic)
        self.mqtt_client.subscribe(topic)

    def publish(self, topic, payload, qos=None):
        if qos is None:
            qos = self.qos
        self.mqtt_client.publish(topic, payload, qos)

    def to_dictionary(self):
        output = {}
        output['server'] = self.server
        output['id'] = self.id
        output['keep_alive'] = self.keep_alive
        output['qos'] = self.qos
        output['ca_cert'] = self.ca_cert

        return  output

    def run(self):
        self.trace.info('started')

        if self.user_id is not None and len(self.user_id) != 0:
            self.trace.debug('Secure Mode :', self.user_id, self.user_pw)
            self.mqtt_client.username_pw_set(self.user_id, self.user_pw)

        if len(self.server['ca_cert']) != 0:
            self.trace.info('CA Cert applied :', self.server['ca_cert'])
            self.mqtt_client.tls_set(ca_certs=self.server['ca_cert'])

        self.mqtt_client.connect(self.server['url'], self.server['port'], self.keep_alive)

        self.mqtt_client.loop_forever()

    @staticmethod
    def mqtt_client_on_connect(client, self, flags, rc):
        self.connected = True
        if self.on_connect is not None:
            self.on_connect(self.parent, flags, rc)
        self.trace.info('Connected with result code :' + str(rc))

    @staticmethod
    def mqtt_client_on_disconnect(client, self, rc):
        self.connected = False
        if self.on_disconnect is not None:
            self.on_disconnect(self.parent, rc)
        self.trace.info('Disonnected with result code :' + str(rc))

    @staticmethod
    def mqtt_client_on_message(client, self, message):
        if self.on_message is not None:
            self.on_message(self.parent, message.topic, message.payload.decode('utf-8'))

    @staticmethod
    def mqtt_client_on_publish(client, self, mid):
        if self.on_publish is not None:
            self.on_publish(self.parent, mid)

    @staticmethod
    def mqtt_client_on_log(client, self, level, buf):
        if self.on_log is not None:
            self.on_log(self.parent, level, buf)
        None
