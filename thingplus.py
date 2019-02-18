import threading
import paho.mqtt.client as mqtt

class   Server(threading.Thread):
    def __init__(self, config = None):
        threading.Thread.__init__(self)
        self.url = 'mqtt.thingplus.net'
        self.port = 8883
        self.ca_cert = './ca-cert.pem'
        self.keep_alive = 60
        self.gateway_list = []

        if config is not None:
            if config.get('url') is not None:
                self.url = config.get('url')

            if config.get('port') is not None:
                self.port = config.get('port')

            if config.get('ca_cert') is not None:
                self.ca_cert = config.get('ca_cert')

            if config.get('keep_alive') is not None:
                self.keep_alive = config.get('keep_aplive')

    def attach(self, gateway):
        for item in self.gateway_list:
            if Gateway.match(gateway, item) == True:
                return  False
        self.gateway_list.append(gateway)
        gateway.attach(self)

    def run(self):
        for gateway in self.gateway_list:
            gateway.start()

    def print_config(self):
        print('[ {0:s} ]'.format('SERVER'))
        print('{0:>12s} : {1:s}'.format('url', self.url))
        print('{0:>12s} : {1:s}'.format('port', str(self.port)))
        print('{0:>12s} : {1:s}'.format('ca_cert', self.ca_cert))
        print('{0:>12s} : {1:s}'.format('keep_alive', str(self.keep_alive)))
        print('{0:>12s} : {1:s}'.format('Gateways', str(len(self.gateway_list))))
        for gateway in self.gateway_list:
            gateway.print_config(4)

class   Gateway(threading.Thread):
    def __init__(self, config = None):
        threading.Thread.__init__(self)
        self.id = None 
        self.apikey = None
        self.qos = 0
        self.device_list = []

        if config is not None:
            if config.get('id') is not None:
                self.id = config.get('id')

            if config.get('apikey') is not None:
                self.apikey = config.get('apikey')

            if config.get('devices') is not None:
                for item in config.get('devices'):
                    device = Device(item)
                    self.attach(device)

    @staticmethod
    def match(a, b):
        return  (a.id == b.id)

    @staticmethod
    def on_connect(gateway, user_data, flags, rc):
        print('Connected with result code' + str(rc))

    @staticmethod
    def on_message(gateway, user_data, message):
        print(message.topic + ' ' + str(message.payload))

    @staticmethod
    def on_log(gateway, user_data, level, buf):
        print(buf)

    def init(self):
        self.mqtt_client = mqtt.Client(self.id)
        self.mqtt_client.username_pw_set(self.id, self.apikey)

        self.mqtt_client.on_connect = Gateway.on_connect
        self.mqtt_client.on_message = Gateway.on_message
        self.mqtt_client.on_log = Gateway.on_log

        #self.mqtt_client.enable_logger(mqtt.MQTT_LOG_DEBUG)

    def run(self):
        self.init()

        if hasattr(self, 'server'):
            self.mqtt_client.tls_set(ca_certs=self.server.ca_cert)
            self.mqtt_client.connect(self.server.url, self.server.port, self.server.keep_alive)

        self.mqtt_client.loop_forever()

    def attach(self, item):
        if isinstance(item, Server):
            self.server = item
        elif isinstance(item, Device):
            self.device_list.append(item)

    def sub(self, topic):
        self.mqtt_client.subscribe(topic)

    def pub(self, topic, payload, qos=None):
        if qos is None:
            qos = self.qos
        self.mqtt_client.publish(topic, payload, qos)

    def print_config(self, indent = 0):
        output_format = '{0:>'+str(10+indent)+'s} : {1:s}'
        print(output_format.format('id', self.id))
        print(output_format.format('apikey', self.apikey))
        print(output_format.format('Devices', str(len(self.device_list))))
        for device in self.device_list:
            device.print_config(indent+4)


class   Device():
    def __init__(self, config = None):
        self.id = None
        self.sensor_list = []

        if config is not None:
            if config.get('id') is not None:
                self.id = config.get('id')

            if config.get('sensors') is not None:
                for item in config.get('sensors'):
                    sensor = Sensor(item)
                    self.attach(sensor)

    @staticmethod
    def match(a, b):
        return  (a.id == b.id)

    def attach(self, sensor):
        for item in self.sensor_list:
            if Sensor.match(sensor, item) == True:
                return  False
        self.sensor_list.append(sensor)
        sensor.attach(self)

    def single_run(self):
        for sensor in self.sensor_list:
            sensor.single_run()

    def print_config(self, indent = 0):
        output_format = '{0:>'+str(10+indent)+'s} : {1:s}'
        print(output_format.format('id', self.id))
        print(output_format.format('Sensors', str(len(self.sensor_list))))
        for sensor in self.sensor_list:
            sensor.print_config(indent+4)

class   Sensor():
    def __init__(self, config = None):
        self.id = 0
        self.value = 0

        if config is not None:
            if config.get('id') is not None:
                self.id = config.get('id')

    @staticmethod
    def match(a, b):
        return  (a.id == b.id)

    def attach(self, device):
        self.device = device

    def single_run(self):
        None

    def print_config(self, indent = 0):
        output_format = '{0:>'+str(10+indent)+'s} : {1:s}'
        print(output_format.format('id', self.id))
