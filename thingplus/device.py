import trace
import thingplus.sensor as Sensor

class   Device():
    def __init__(self, config = None, parent = None):
        self.parent = parent
        self.id = None
        self.sensor_list = []
        self.sensor_models = {
            'voltage' : Sensor.Voltage,
            'percent' : Sensor.Percent,
            'weight' : Sensor.Weight,
            'temperature' : Sensor.Temperature,
            'pressure' : Sensor.Pressure,
            'current' : Sensor.Current,
            'vibration' : Sensor.Vibration,
            'percent' : Sensor.Percent,
            'number' : Sensor.Number,
            'onoff' : Sensor.OnOff
        }

        self.trace = trace.Trace(self)
        self.trace.name = 'DE'

        if config is not None:
            self.set_config(config)

        self.trace.info('Device created')

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

            self.trace.info('Add new sensor :', sensor.id) 
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