import trace
import random
import time

def create(model = None, config = None, parent = None):
    if model is None:
        return  Sensor(config = config, parent = parent)
    else:
        return  model(config = config, parent = parent)
    
    return  sensor

class   Sensor():
    def __init__(self, config = None, parent = None):
        self.parent = parent
        self.id = None
        self.model = None
        self.type = 'int'
        self.time = 0
        self.value = 0
        self.min = 0
        self.max = 100
        self.unit = ''
        self.trace = trace.Trace(self)
        self.trace.name = 'SE'
        self.direction = 1

        if config is not None:
            self.set_config(config)

    def set_config(self, config):
        try:
            if config.get('id') is not None:
                self.id = config.get('id')
    
            if config.get('model') is not None:
                self.model = config.get('model')
   
            if config.get('type') is not None:
                self.type = config.get('type')
  
            if config.get('min') is not None:
                self.min = config.get('min')
  
            if config.get('max') is not None:
                self.max = config.get('max')
 
            if config.get('scale') is not None:
                self.scale = config.get('scale')

            if config.get('unit') is not None:
                self.unit = config.get('unit')

            return  True
        except Exception as error:
            self.trace.error(error)
    
        return  False

    def single_run(self):
        self.simulation_run()
        None

    def simulation_run(self):
        if self.model == 'onoff':
            if random.random() > 0.5:
                self.value = self.max
            else:
                self.value = self.min
        else:
            ratio  = random.random() * 0.1

        value = self.value + (self.max - self.min) * ratio * self.direction
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

    def to_dictionary(self):
        output={}
        output['id'] = self.id
        output['model'] = self.model

        return  output


class   Voltage(Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, config, parent)
        self.model = 'voltage'
        self.type = 'float'
        self.min = 0
        self.max = 5
        self.unit = 'V'

class   Percent(Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, config, parent)
        self.model = 'percent'
        self.type = 'float'
        self.min = 0
        self.max = 100
        self.unit = '%'


class   Weight(Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, config, parent)
        self.model = 'weight'
        self.type = 'float'
        self.min = 0
        self.max = 150
        self.unit = 'kg'


class   Temperature(Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, config, parent)
        self.type = 'temperature'
        self.min = 0
        self.max = 100
        self.scale = 1
        self.unit = 'C'

class   Current(Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, config, parent)
        self.type = 'current'
        self.min = 0
        self.max = 100
        self.scale = 1
        self.unit = 'A'


class   Pressure(Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, config, parent)
        self.type = 'pressure'
        self.min = 0
        self.max = 10000
        self.scale = 1
        self.unit = 'kg/cm2'

class   Vibration(Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, config, parent)
        self.type = 'vibration'
        self.min = 0
        self.max = 10000
        self.scale = 1
        self.unit = ''

class   Percent(Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, config, parent)
        self.type = 'percent'
        self.min = 0
        self.max = 1000
        self.scale = 0.1
        self.unit = ''

class   Number(Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, config, parent)
        self.type = 'number'
        self.min = 0
        self.max = 1000
        self.scale = 0.1
        self.unit = ''

class   OnOff(Sensor):
    def __init__(self, config = None, parent = None):
        Sensor.__init__(self, config, parent)
        self.type = 'onoff'
        self.min = 0
        self.max = 1
        self.scale = 1