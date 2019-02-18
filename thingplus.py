import threading
import paho.mqtt.client as mqtt

class   Client(threading.Thread):
    def __init__(self, config = None):
        threading.Thread.__init__(self)
        self.url = 'mqtt.thingplus.net'
        self.port = 8883
        self.ca_cert = './ca-cert.pem'
        self.keep_alive = 60
        self.client_id= ''
        self.user_id= None
        self.user_pw= None
        self.qos = 0

        if config is not None:
            if config.get('url') is not None:
                self.url = config.get('url')

            if config.get('port') is not None:
                self.port = config.get('port')

            if config.get('ca_cert') is not None:
                self.ca_cert = config.get('ca_cert')

            if config.get('keep_alive') is not None:
                self.keep_alive = config.get('keep_aplive')

            if config.get('client_id') is not None:
                self.client_id = config.get('client_id')

            if config.get('user_id') is not None:
                self.user_id = config.get('user_id')

            if config.get('user_pw') is not None:
                self.user_pw = config.get('user_pw')


    @staticmethod
    def on_connect(client, user_data, flags, rc):
        print('Connected with result code' + str(rc))

    @staticmethod
    def on_message(client, user_data, message):
        print(message.topic + ' ' + str(message.payload))

    @staticmethod
    def on_log(client, user_data, level, buf):
        print(buf)

    def init(self):
        self.mqtt_client = mqtt.Client(self.client_id)
        if self.user_id is not None:
            self.mqtt_client.username_pw_set(self.user_id, self.user_pw)

        self.mqtt_client.on_connect = Client.on_connect
        self.mqtt_client.on_message = Client.on_message
        self.mqtt_client.on_log = Client.on_log
        #self.mqtt_client.enable_logger(mqtt.MQTT_LOG_DEBUG)

    def run(self):
        self.init()
        self.mqtt_client.tls_set(ca_certs=self.ca_cert)

        self.mqtt_client.connect(self.url, self.port, self.keep_alive)

        self.mqtt_client.loop_forever()

    def sub(self, topic):
        self.mqtt_client.subscribe(topic)

    def pub(self, topic, payload, qos=None):
        if qos is None
            qos = self.qos
        self.mqtt_client.publish(topic, payload, qos)

    def print(self):
        print('url : ', self.url)
        print('port : ', self.port)
        print('ca_cert : ', self.ca_cert)
        print('keep_alive : ', self.keep_alive)
        print('client_id : ', self.client_id)
        print('user_id : ', self.user_id)
        print('user_pw : ', self.user_pw)