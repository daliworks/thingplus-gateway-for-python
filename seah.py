import thingplus

class   Gateway(thingplus.Gateway):
    def __init__(self, config):
        thingplus.Gateway.__init__(self, config)

    def init(self):
        thingplus.Gateway.init(self)

    def run(self):
        sensor_list = []
        thingplus.Gateway.run(self)

        for device in self.device_list:
            sensor_list = sensor_list + device.sensor_list

        while True:
            for sensor in sensor_list:
                sensor.single_run()