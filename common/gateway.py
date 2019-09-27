import json
import threading
import trace
import time
import server.base as Server
from common.device import Device

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

class   Gateway(threading.Thread):
    def __init__(self, _config = None):
        threading.Thread.__init__(self)
        self.config = {
            'id' : None,
            'apikey' : None,
            'keep_alive' : 60,
            'collection_interval' : 10,
            'transmission_interval' : 60,
            'transmission_gap' : 0.1,
            'client' : {
                    'id' : '',
                    'user_id' : '',
                    'user_pw' : '',
                    'server' : {
                            'url' : '',
                            'port' : 80,
                            'ca_cert' : ''
                        }
                }
        }
            
        self.client = None
        self.device_list = []
        self.device_models = {
            'default' : Device
        }
        self.trace = trace.Trace(self)
        self.trace.name = 'GW'
        self.sensor_list = []

        self.keep_alive_timer = None
        self.collection_timer = None
        self.transmission_timer = None
        self.status_transmission_timer = None

        self.set_config(_config)


        self.trace.info('Gateway created')

    def set_config(self, _config):
        if _config is not None:
            try:
                self.config.update(_config)

                self.config['client']['server'] = self.config['server']
   
                if _config.get('client') is not None:
                    if _config['client'].get('id') is None:
                        self.config['client']['id'] = self.config['id']

                    if _config['client'].get('user_id') is None:
                        self.config['client']['user_id'] = self.config['id']

                    if _config['client'].get('user_pw') is None:
                        self.config['client']['user_pw'] = self.config['apikey']
                else: 
                    self.config['client']['id'] = self.config['id']
                    self.config['client']['user_id'] = self.config['id']
                    self.config['client']['user_pw'] = self.config['apikey']
    
                return  True
            except Exception as error:
                self.trace.error('Except : %s'%error)
    
        return  False

    def init(self):
        for device_config in self.config['devices']:
            self.trace.debug(device_config)
            self.add_device(device_config)


    def stage1(self):
        self.init()

        if self.server is not None:
            self.client = self.server.create_client(_config = self.config['client'], _parent = self)
            self.client.on_connect = Gateway.client_on_connect
            self.client.on_disconnect = Gateway.client_on_disconnect
            self.client.on_message = Gateway.client_on_message
            self.client.on_publish = Gateway.client_on_publish

        try:
            if self.collection_timer is not None:
                self.collection_timer.stop()
        except Exception as error:
            self.trace.error(error)

        try:
            if self.keep_alive_timer is not None:
                self.keep_alive_timer.stop()
        except Exception as error:
            self.trace.error(error)

        try:
            if self.transmission_timer is not None:
                self.transmission_timer.stop()
        except Exception as error:
            self.trace.error(error)

    def stage2(self):
        if self.client is not None:
            self.client.start()

    def stage3(self):
        def keep_alive(self):
            self.publish_gateway_and_sensor_status()
    
        def sensor_collection(self):
            for sensor in self.sensor_list:
                sensor.single_run()

        def sensor_transmission(self):
            if self.client.is_connected():
                self.trace.info('tramsmission start!')
                transmission_start_time = time.time()
                start_time = time.time()

                for sensor in self.sensor_list:
                    self.publish_sensor_value(sensor)

                    current_time = time.time()
                    start_time += self.config['transmission_gap']
                    if start_time > time.time():
                        time.sleep(start_time - time.time())

                self.trace.info('Elapsed Time : {0:5.2f}'.format(time.time() - transmission_start_time))

        self.sensor_list = []
        for device in self.device_list:
            self.sensor_list = self.sensor_list + device.sensor_list

        self.collection_timer = RepeatedTimer(self.config['collection_interval'], sensor_collection, self)
        self.collection_timer.start()

        self.keep_alive_timer = RepeatedTimer(self.config['keep_alive'], keep_alive, self)
        self.keep_alive_timer.start()

        self.transmission_timer = RepeatedTimer(self.config['transmission_interval'], sensor_transmission, self)
        self.transmission_timer.start()

    def run(self):
        self.trace.info('started')
        self.stage1()
        self.stage2()
        self.stage3()

        for device in self.device_list:
            device.start()

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

        self.trace.info('Device creation success :', model)
        self.attach(device)
        return  True

    def attach(self, item):
        if isinstance(item, Server.Server):
            self.server = item
            self.trace.info('Server attached')
        elif isinstance(item, Device):
            self.device_list.append(item)
            self.trace.info('New device[%s] attached'%(item.get_id()))

    def to_dictionary(self): 
        output = self.config
        output['Devices'] = []
        for device in self.device_list:
            output['Devices'].append(device.to_dictionary())

        return  output

    def publish_gateway_status(self):
        topic = 'v/a/g/{0:s}/status'.format(self.config['id'])
        payload = '{0:s},{1:d}'.format('on', int(self.config['keep_alive'] * 1.5))
        self.client.publish(topic, payload)
 
    def publish_gateway_and_sensor_status(self):
        topic = 'v/a/g/{0:s}/status'.format(self.config['id'])
        payload = '{0:s},{1:d}'.format('on', int(self.config['keep_alive'] * 1.5))
        for sensor in self.sensor_list:
            payload += ',{0:s},{1:s},{2:d}'.format(sensor.id, 'on', int(self.config['keep_alive'] * 1.5))

        self.trace.debug('Keep alive :', payload)
        self.client.publish(topic, payload)
 
    def publish_response(self, msg_id, result = None):
        topic = 'v/a/g/{0:s}/res'.format(self.config['id'])
        payload = {}
        payload['id'] = msg_id
        if result is None:
            payload['result'] = ''
        else:
            payload['result'] = json.dumps(result)
        print(topic, json.dumps(payload))
        self.client.publish(topic, json.dumps(payload))

    def publish_sensor_value(self, sensor):
        value = 0
        decimal_point = 0
        if hasattr(sensor, 'scale'):
            value = sensor.value * sensor.scale
        else:
            value = sensor.value

        topic = 'v/a/g/{0:s}/s/{1:s}'.format(self.config['id'], sensor.id)
        payload = '{0:d},{1:s}'.format(int(sensor.time * 1000), str(value))
        self.client.publish(topic, payload)

    def publish_sensor_status(self, sensor):
        topic = 'v/a/g/{0:s}/s/{1:s}/status'.format(self.config['id'], sensor.id)
        payload = '{0:s},{1:d}'.format('on', int(self.config['keep_alive'] * 1.5))
        self.client.publish(topic, payload)
 
    def on_connect(self, flags, rc):
        topic = 'v/a/g/{0:s}/req'.format(self.config['id'])
        self.client.subscribe(topic)

    def on_disconnect(self, rc):
        None

    def on_message(self, topic, payload):
        self.trace.info(topic + ' ' + payload)

        data = json.loads(payload)

        self.publish_response(data['id'])

    def on_log(self, level, buffer):
        None

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
        self.on_message(topic, payload)
        #self.trace.info(topic + ' ' + payload)

    @staticmethod
    def client_on_publish(self, mid):
        self.on_publish(mid)
        #self.trace.info(' Mid : ', mid)
