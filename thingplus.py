import json
import threading
import paho.mqtt.client as mqtt
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

class   Client(threading.Thread):
    def __init__(self, config = None, parent = None):
        threading.Thread.__init__(self)
        self.parent = parent
        self.id = None 
        self.server = Server()
        self.keep_alive = 60
        self.qos = 0
        self.secure_mode = False
        self.user_id = None
        self.user_pw = None
        self.connected = False
        self.on_connect = None
        self.on_disconnect = None
        self.on_message = None
        self.trace = trace.Trace(self)
        self.trace.name = 'CL'

        self.set_config(config)

        self.mqtt_client = mqtt.Client(client_id = self.id, userdata = self)

        self.mqtt_client.on_connect = Client.mqtt_client_on_connect
        self.mqtt_client.on_disconnect = Client.mqtt_client_on_disconnect
        self.mqtt_client.on_message = Client.mqtt_client_on_message
        self.mqtt_client.on_log = Client.mqtt_client_on_log

    def set_config(self, config):
        if config is not None:
            try:
                if config.get('server') is not None:
                    self.server.set_config(config.get('server'))
    
                if config.get('id') is not None:
                    self.id = config.get('id')
    
                if config.get('keep_alive') is not None:
                    self.keep_alive = config.get('keep_aplive')
    
                if config.get('qos') is not None:
                    self.qos = config.get('qos')
    
                if config.get('secure_mode') is not None:
                    self.secure_mode = config.get('secure_mode')
        
                if config.get('user_id') is not None:
                    self.user_id = config.get('user_id')
    
                if config.get('user_pw') is not None:
                    self.user_pw = config.get('user_pw')
    
                return  True
            except Exception as error:
                self.error(error)

        return  False

    def secure_mode(self, mode = True, user_id = None, user_pw = None):
        self.secure_mode = mode
        self.user_id = user_id
        self.user_pw = user_pw

        self.mqtt_client.username_pw_set(self.user_id, self.user_pw)

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
        output['server'] = self.server.to_dictionary()
        output['id'] = self.id
        output['keep_alive'] = self.keep_alive
        output['qos'] = self.qos
        output['ca_cert'] = self.ca_cert

        return  output

    def run(self):
        self.trace.info('started')

        if self.secure_mode:
            self.trace.debug('Secure Mode :', self.user_id, self.user_pw)
            self.mqtt_client.username_pw_set(self.user_id, self.user_pw)

        if self.server.ca_cert is not None:
            self.trace.info('CA Cert applied :', self.server.ca_cert)
            self.mqtt_client.tls_set(ca_certs=self.server.ca_cert)

        self.mqtt_client.connect(self.server.url, self.server.port, self.keep_alive)

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
    def mqtt_client_on_log(client, self, level, buf):
        self.trace.info(self.id + ' : ' + buf)
        None


class   Gateway(threading.Thread):
    def __init__(self, config = None):
        threading.Thread.__init__(self)
        self.id = None 
        self.apikey = None
        self.collection_interval = 60
        self.transmission_interval = 0.1
        self.client = None
        self.device_list = []
        self.device_models = {
            'default' : Device
        }
        self.trace = trace.Trace(self)
        self.trace.name = 'GW'

        self.set_config(config)

    def set_config(self, config):
        if config is not None:
            try:
                if config.get('id') is not None:
                    self.id = config.get('id')
    
                if config.get('apikey') is not None:
                    self.apikey = config.get('apikey')
    
                if config.get('devices') is not None:
                    for item in config.get('devices'):
                        self.add_device(item)
    
                if config.get('collection_interval') is not None:
                    self.collection_interval = config.get('collection_interval')
    
                if config.get('transmission_interval') is not None:
                    self.transmission_interval = config.get('transmission_interval')
    
                if config.get('server') is not None:
                    client_config = {}
    
                    client_config['server'] = config.get('server')
                    client_config['id'] = self.id
                    client_config['secure_mode'] = True
                    client_config['user_id'] = self.id
                    client_config['user_pw'] = self.apikey
    
                    self.client = Client(config = client_config, parent = self)
                    self.client.on_connect = Gateway.client_on_connect
                    self.client.on_disconnect = Gateway.client_on_disconnect
                    self.client.on_message = Gateway.client_on_message
    
                return  True
            except Exception as error:
                self.trace.error(error)
    
        return  False

    def preprocess(self):
        None

    def postprocess(self):
        None

    def run(self):
        self.trace.info('started')
        self.preprocess()

        if self.client is not None:
            self.client.start()

        self.postprocess()

    def add_device(self, config):
        model = None
        if (config is not None) and (config.get('model') is not None):
            model = self.device_models.get(config.get('model'))
            if model is None:
                self.trace.error('Model not found :', config.get('model'))
                self.trace.error('Device Models :', self.device_models)
                return  False

        device = Device.create(model = model, config = config, parent = self)
        if device is None:
            self.trace.error('Device creation failed :', model)
            return  False

        self.attach(device)
        return  True

    def attach(self, item):
        if isinstance(item, Server):
            self.server = item
        elif isinstance(item, Device):
            self.device_list.append(item)

    def to_dictionary(self): 
        output = {}
        output['id'] = self.id
        output['apikey'] = self.apikey
        output['Devices'] = []
        for device in self.device_list:
            output['Devices'].append(device.to_dictionary())

        return  output

    def publish_response(self, msg_id, result = None):
        topic = 'v/a/g/{0:s}/res'.format(self.id)
        payload = {}
        payload['id'] = msg_id
        if result is None:
            payload['result'] = ''
        else:
            payload['result'] = json.dumps(result)
        print(topic, json.dumps(payload))
        self.client.publish(topic, json.dumps(payload))

    def publish_sensor_value(self, sensor):
        topic = 'v/a/g/{0:s}/s/{1:s}'.format(self.id, sensor.id)
        payload = '{0:d},{1:s}'.format(int(sensor.time * 1000), str(sensor.value))
        self.client.publish(topic, payload)

    def publish_sensor_status(self, sensor):
        topic = 'v/a/g/{0:s}/s/{1:s}/status'.format(self.id, sensor.id)
        payload = '{0:d},{1:s}'.format(90, 'on')
        self.client.publish(topic, payload)
 
    def on_connect(self, flags, rc):
        topic = 'v/a/g/{0:s}/req'.format(self.id)
        self.client.subscribe(topic)

    def on_disconnect(self, rc):
        None

    def on_message(self, topic, payload):
        self.trace.info(topic + ' ' + payload)

        data = json.loads(payload)

        self.publish_response(data['id'])

    @staticmethod
    def create(config = None):
        try:
            return  Gateway(config)
        except Exception as error:
            return  None

    @staticmethod
    def client_on_connect(self, flags, rc):
        self.on_connect(flags, rc)
        self.trace.info('Connected with result code :' + str(rc))

    @staticmethod
    def client_on_disconnect(self, rc):
        self.on_disconnect(rc)
        self.trace.info('Disonnected with result code :' + str(rc))

    @staticmethod
    def client_on_message(self, topic, payload):
        self.trace.info(topic + ' ' + payload)
        self.on_message(topic, payload)

class   Device():
    def __init__(self, config = None, parent = None):
        self.parent = parent
        self.id = None
        self.sensor_list = []
        self.sensor_models = {
            'default' : Sensor
        }
        self.trace = trace.Trace(self)
        self.trace.name = 'DE'

        if config is not None:
            self.set_config(config)

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

            return  True 
        except Exception as error:
            self.trace.error('Err :', error)

        return  False

    def add_sensor(self, config):
        try:
            model = None
            if (config is not None) and (config.get('model') is not None):
                model = self.sensor_models.get(config.get('model'))
                if model is None:
                    self.trace.error('Model not found :', config.get('model'))
                    return  False
    
            sensor = Sensor.create(model = model, config = config, parent = self)
            if sensor is None:
                self.trace.error('Sensor creation failed :', config)
                return  False
    
            self.attach(sensor)
        except Exception as error:
            self.trace.error('add_sensor :', error)
            return  False

        return  True

    def attach(self, sensor):
        for item in self.sensor_list:
            if sensor.id == item.id:
                return  False
        self.sensor_list.append(sensor)

    def single_run(self):
        for sensor in self.sensor_list:
            sensor.single_run()

    def to_dictionary(self):
        output = {}
        output['id'] = self.id
        output['Sensors'] = []
        for sensor in self.sensor_list:
            output['Sensors'].append(sensor.to_dictionary())

        return  output

    @staticmethod
    def create(model = None, config = None, parent = None):
        if model is None:
            device = Device(config, parent)
        else:
            device = model(config, parent)
    
        return  device

class   Sensor():
    def __init__(self, config = None, parent = None):
        self.parent = parent
        self.id = None
        self.type = None
        self.simulation = False
        self.time = 0
        self.value = 0
        self.min = 0
        self.max = 100
        self.unit = ''
        self.trace = trace.Trace(self)
        self.trace.name = 'SE'

        if config is not None:
            self.set_config(config)

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

            if config.get('unit') is not None:
                self.unit = config.get('unit')

            return  True
        except Exception as error:
            self.trace.error(error)
    
        return  False

    def single_run(self):
        None

    def to_dictionary(self):
        output={}
        output['id'] = self.id
        output['type'] = self.type

        return  output

    @staticmethod
    def create(model = None, config = None, parent = None):
        if model is None:
            return  Sensor(config = config, parent = parent)
        else:
            return  model(config = config, parent = parent)
    
        return  sensor

class   SensorSimulator(thingplus.Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, parent = parent)
        self.simulation = True
        self.direction = 1
        self.type = 'number'
        self.min = 0
        self.max = 100
        self.scale = 1

        self.set_config(config)

    def single_run(self):
        if self.simulation:
            if self.type == 'onoff':
                if random.random() > 0.5:
                    self.value = self.max
                else:
                    self.value = self.min
            else:
                value = self.value + int((self.max - self.min) * random.random() * 0.1)
                if self.direction > 0:
                    if self.max > value:
                        self.value = value
                    else:
                        self.value = self.max
                        self.direction = -1
                else:
                    if self.min < value:
                        self.value = value
                    else:
                        self.value = self.min
                        self.direction = 1
            self.time = int(time.time())
        #self.trace.info('{0:d}, {1:s}'.format(self.time, str(self.value)))
 