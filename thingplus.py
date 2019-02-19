import json
import threading
import paho.mqtt.client as mqtt

class   Server(threading.Thread):
    def __init__(self, config = None):
        threading.Thread.__init__(self)
        self.parent = None
        self.id = None
        self.url = 'mqtt.thingplus.net'
        self.port = 8883
        self.secure_mode = True
        self.ca_cert = './ca-cert.pem'
        self.keep_alive = 60
        self.client_id = None 
        self.user_id = None
        self.user_pw = None
        self.qos = 0
        self.connected = False

        if config is not None:
            if config.get('url') is not None:
                self.url = config.get('url')

            if config.get('port') is not None:
                self.port = config.get('port')

            if config.get('ca_cert') is not None:
                self.ca_cert = config.get('ca_cert')

            if config.get('keep_alive') is not None:
                self.keep_alive = config.get('keep_aplive')

    @staticmethod
    def on_connect(client, server, flags, rc):
        server.connected = True
        print('Connected with result code' + str(rc))

    @staticmethod
    def on_disconnect(client, server, rc):
        server.connected = False
        print('Disonnected with result code' + str(rc))

    @staticmethod
    def on_message(client, server, message):
        print(message.topic + ' ' + str(message.payload))

    @staticmethod
    def on_log(client, server, level, buf):
        print(server.id + ' : ' + buf)
        None

    def init(self):
        self.mqtt_client = mqtt.Client(client_id = self.client_id, userdata = self)
        self.mqtt_client.username_pw_set(self.user_id, self.user_pw)

        self.mqtt_client.on_connect = Server.on_connect
        self.mqtt_client.on_disconnect = Server.on_disconnect
        self.mqtt_client.on_message = Server.on_message
        self.mqtt_client.on_log = Server.on_log

    def run(self):
        self.init()

        if self.secure_mode:
            self.mqtt_client.tls_set(ca_certs=self.ca_cert)
            self.mqtt_client.connect(self.url, self.port, self.keep_alive)

        self.mqtt_client.loop_forever()

    def sub(self, topic):
        self.mqtt_client.subscribe(topic)

    def pub(self, topic, payload, qos=None):
        if qos is None:
            qos = self.qos
        self.mqtt_client.publish(topic, payload, qos)

    def to_json(self):
        output = {}
        output['url'] = self.url
        output['port'] = self.port
        output['ca_cert'] = self.ca_cert
        output['keep_alive'] = self.keep_alive
        output['Gateways'] = []
        for gateway in self.gateway_list:
            output['Gateways'].append(json.loads(gateway.to_json()))
        return  json.dumps(output, indent=4) 

class   Gateway(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.id = None 
        self.apikey = None
        self.qos = 0
        self.collection_interval = 60
        self.transmission_interval = 0.1
        self.server = None
        self.server_id = None
        self.device_list = []
        self.device_models = {
            'default' : Device
        }

    @staticmethod
    def match(a, b):
        return  (a.id == b.id)

    def set_config(self, config):
        try:
            if config.get('id') is not None:
                self.id = config.get('id')

            if config.get('apikey') is not None:
                self.apikey = config.get('apikey')

            if config.get('devices') is not None:
                for item in config.get('devices'):
                    self.add_device(item)

            if config.get('server_id') is not None:
                self.server_id = config.get('server_id')

            if config.get('collection_interval') is not None:
                self.collection_interval = config.get('collection_interval')

            if config.get('transmission_interval') is not None:
                self.transmission_interval = config.get('transmission_interval')

        except Exception as error:
            print(self.__class__.__name__, error)

    def run(self):
        print('Gateway[{0:s}] started', self.id)
        if self.server is not None:
            self.server.client_id = self.id
            self.server.user_id = self.id
            self.server.user_pw = self.apikey

            self.server.start()

    def add_device(self, config):
        model = None
        if (config is not None) and (config.get('model') is not None):
            model = self.device_models.get(config.get('model'))
            if model is None:
                return  False

        device = create_device(config = config, model = model, parent = self)
        if device is None:
            return  False

        self.attach(device)
        return  True

    def attach(self, item):
        if isinstance(item, Server):
            self.server = item
        elif isinstance(item, Device):
            self.device_list.append(item)

    def to_json(self): 
        output = {}
        output['id'] = self.id
        output['apikey'] = self.apikey
        output['Devices'] = []
        for device in self.device_list:
            output['Devices'].append(json.loads(device.to_json()))

        return  json.dumps(output)

def create_gateway(config = None):
    gateway = Gateway()

    if config is not None:
        gateway.set_config(config)

    return  gateway

class   Device():
    def __init__(self, parent = None):
        self.parent = parent
        self.id = None
        self.sensor_list = []
        self.sensor_models = {
            'default' : Sensor
        }

    @staticmethod
    def match(a, b):
        return  (a.id == b.id)

    def set_config(self, config):
        try:
            if config.get('id') is not None:
                self.id = config.get('id')

            if config.get('sensors') is not None:
                if type(config.get('sensors')) is list:
                    for item in config.get('sensors'):
                        self.add_sensor(item)
                elif type(config.get('sensors')) is str:
                    if config.get('sensors') == 'predefined':
                        if hasattr(self, 'predefined_sensors'):
                            for item in self.predefined_sensors:
                                self.add_sensor(item)

        except Exception as error:
            print(self.__class__.__name__, error)

    def add_sensor(self, config):
        model = None
        if (config is not None) and (config.get('model') is not None):
            model = self.sensor_models.get(config.get('model'))
            if model is None:
                return  False

        sensor = create_sensor(config = config, model = model, parent = self)
        if sensor is None:
            return  False

        self.attach(sensor)
        return  True

    def attach(self, sensor):
        for item in self.sensor_list:
            if Sensor.match(sensor, item) == True:
                return  False
        self.sensor_list.append(sensor)

    def single_run(self):
        for sensor in self.sensor_list:
            sensor.single_run()

    def to_json(self):
        output = {}
        output['id'] = self.id
        output['Sensors'] = []
        for sensor in self.sensor_list:
            output['Sensors'].append(json.loads(sensor.to_json()))

        return  json.dumps(output)

def create_device(config = None, model = None, parent = None):
    if model is None:
        device = Device(parent)
    else:
        device = model(parent)

    if config is not None:
        device.set_config(config)

    return  device

class   Sensor():
    def __init__(self, parent = None):
        self.parent = parent
        self.id = None
        self.type = None
        self.simulation = False
        self.time = 0
        self.value = 0
        self.min = 0
        self.max = 100
        self.unit = ''

    @staticmethod
    def match(a, b):
        return  (a.id == b.id)

    def set_config(self, config):
        try:
            if config.get('id') is not None:
                self.id = config.get('id')

            if config.get('type') is not None:
                self.type = config.get('type')

            if config.get('min') is not None:
                self.min = config.get('min')

            if config.get('max') is not None:
                self.max = config.get('max')

            if config.get('type') is not None:
                self.scale = config.get('scale')

        except Exception as error:
            print(self.__class__.__name__, error)

    def single_run(self):
        None

        print(self.id, self.value)

    def to_json(self):
        output={}
        output['id'] = self.id
        output['type'] = self.type
        return  json.dumps(output)

def create_sensor(config = None, model = None, parent = None):
    sensor = None
    if model is None:
        sensor = Sensor(parent)
    else:
        sensor = model(parent)

    if config is not None:
        sensor.set_config(config)

    return  sensor

 