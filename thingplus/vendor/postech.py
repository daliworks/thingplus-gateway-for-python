import thingplus.gateway
import thingplus.device
import thingplus.sensor
import copy
import random
import time
import json
import trace

class   Gateway(thingplus.gateway.Gateway):
    def __init__(self, config = None):
        thingplus.gateway.Gateway.__init__(self)
        self.collection_start_time = None
        self.device_models = {
            'health_monitor' : HealthMonitor
        }

        self.set_config(config)

    def add_device(self, config):
        try:
            new_config = copy.copy(config)
            new_config['id'] = self.id + '-hm'
    
            thingplus.gateway.Gateway.add_device(self, new_config)
        except Exception as error:
            self.trace.error(error)

    @staticmethod
    def create(config = None):
        trace.info('Create postech')
        try:
            return  Gateway(config)
        except Exception as error:
            trace.error(error)
            return  None

class   HealthMonitor(thingplus.device.Device):
    def __init__(self, config = None, parent = None):
        thingplus.device.Device.__init__(self, parent = parent)
        self.predefined_sensors = [
            { 'id' : 'egcppg', 'model' : 'voltage', 'type' : 'float', 'min' : 0, 'max' : 5, 'scale' : 1},
            { 'id' : 'bodyfat', 'model' : 'percent', 'type' : 'float', 'min' : 0, 'max' : 100, 'scale' : 1},
            { 'id' : 'weight', 'model' : 'weight', 'type' : 'float', 'min' : 0, 'max' : 150, 'scale' : 1}
        ];

        self.set_config(config)

    def add_sensor(self, config):
        try:
            new_config = copy.copy(config)
            new_config['id'] = self.id + '-' + config['id']
    
            thingplus.device.Device.add_sensor(self, new_config)
        except Exception as error:
            self.trace.error(error)


