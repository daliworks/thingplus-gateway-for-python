import thingplus
import copy
import random
import time

class   Gateway(thingplus.Gateway):
    def __init__(self):
        thingplus.Gateway.__init__(self)
        self.device_models = {
            'turbo_compressor' : TurboCompressor,
            'turbo_blower' : TurboBlower
        }

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

            if self.server.connected:
                print('[{0:s}] Gateway[{1:s}] tramsmission start!'.format(str(int(time.time())), self.id))
                transmission_start_time = time.time()
                start_time = time.time()
                for sensor in sensor_list:
                    topic = 'v/a/g/' + self.id + '/s/' + sensor.id
                    payload = str(sensor.time * 1000) + ',' + str(sensor.value)
                    self.server.pub(topic, payload)
                    current_time = time.time()
                    if current_time - start_time < self.transmission_interval:
                        time.sleep(self.transmission_interval - (current_time - start_time))
                    start_time = start_time + self.transmission_interval
                transmission_finished_time = time.time()
                print('[{0:s}] Gateway[{1:s}] Elapsed Time : {2:d}'.format(str(int(time.time())), self.id, int(transmission_finished_time - transmission_start_time)))

            time.sleep(self.collection_interval)


def create_gateway(config = None):
    gateway = Gateway()

    if config is not None:
        gateway.set_config(config)

    return  gateway

class   TurboCompressor(thingplus.Device):
    def __init__(self, parent = None):
        thingplus.Device.__init__(self, parent)
        self.sensor_models = {
            'temperature' : Temperature,
            'pressure' : Pressure,
            'current' : Current,
            'vibration' : Vibration,
            'percent' : Percent,
            'number' : Number,
            'onoff' : OnOff
        }
        self.predefined_sensors = [
            { 'id' : '36000', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36001', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36002', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36003', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36004', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36005', 'model' : 'percent', 'min' : 0, 'max' : 1000, 'scale' : 0.1},
            { 'id' : '36006', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36007', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36008', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36009', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36010', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36011', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36012', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36013', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36014', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36015', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36016', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36017', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36018', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36019', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36020', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36021', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36022', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36023', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36024', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36025', 'model' : 'number', 'min' : 0, 'max' : 1000, 'scale' : 0.1},
            { 'id' : '36026', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36027', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36028', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36029', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36030', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36031', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36032', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36033', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36034', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36035', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '46100', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46101', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46102', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46103', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46104', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46105', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46106', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46107', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46108', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46109', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46110', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46111', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46112', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46113', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46114', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46115', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46116', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46117', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '46118', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '46119', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '46120', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '46121', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '46122', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '10080', 'model' : 'onoff'},
            { 'id' : '10081', 'model' : 'onoff'},
            { 'id' : '10082', 'model' : 'onoff'},
            { 'id' : '10083', 'model' : 'onoff'},
            { 'id' : '10084', 'model' : 'onoff'},
            { 'id' : '10085', 'model' : 'onoff'},
            { 'id' : '10086', 'model' : 'onoff'},
            { 'id' : '10087', 'model' : 'onoff'},
            { 'id' : '10096', 'model' : 'onoff'},
            { 'id' : '10097', 'model' : 'onoff'},
            { 'id' : '10098', 'model' : 'onoff'},
            { 'id' : '10099', 'model' : 'onoff'},
            { 'id' : '10100', 'model' : 'onoff'},
            { 'id' : '10101', 'model' : 'onoff'},
            { 'id' : '10102', 'model' : 'onoff'},
            { 'id' : '10112', 'model' : 'onoff'},
            { 'id' : '10113', 'model' : 'onoff'},
            { 'id' : '10114', 'model' : 'onoff'},
            { 'id' : '10115', 'model' : 'onoff'},
            { 'id' : '10116', 'model' : 'onoff'},
            { 'id' : '10117', 'model' : 'onoff'},
            { 'id' : '10118', 'model' : 'onoff'},
            { 'id' : '10119', 'model' : 'onoff'},
            { 'id' : '10128', 'model' : 'onoff'},
            { 'id' : '10129', 'model' : 'onoff'},
            { 'id' : '10130', 'model' : 'onoff'},
            { 'id' : '10131', 'model' : 'onoff'},
            { 'id' : '10132', 'model' : 'onoff'},
            { 'id' : '10133', 'model' : 'onoff'},
            { 'id' : '10134', 'model' : 'onoff'},
            { 'id' : '10135', 'model' : 'onoff'},
            { 'id' : '10144', 'model' : 'onoff'},
            { 'id' : '10145', 'model' : 'onoff'},
            { 'id' : '10146', 'model' : 'onoff'},
            { 'id' : '10147', 'model' : 'onoff'},
            { 'id' : '10148', 'model' : 'onoff'},
            { 'id' : '10149', 'model' : 'onoff'},
            { 'id' : '10150', 'model' : 'onoff'},
            { 'id' : '10151', 'model' : 'onoff'},
            { 'id' : '10160', 'model' : 'onoff'},
            { 'id' : '10161', 'model' : 'onoff'},
            { 'id' : '10162', 'model' : 'onoff'},
            { 'id' : '10163', 'model' : 'onoff'},
            { 'id' : '10164', 'model' : 'onoff'},
            { 'id' : '10165', 'model' : 'onoff'},
            { 'id' : '10166', 'model' : 'onoff'},
            { 'id' : '10167', 'model' : 'onoff'},
            { 'id' : '10176', 'model' : 'onoff'},
            { 'id' : '10177', 'model' : 'onoff'},
            { 'id' : '10178', 'model' : 'onoff'},
            { 'id' : '10179', 'model' : 'onoff'},
            { 'id' : '10180', 'model' : 'onoff'},
            { 'id' : '10181', 'model' : 'onoff'},
            { 'id' : '10182', 'model' : 'onoff'},
            { 'id' : '10183', 'model' : 'onoff'},
            { 'id' : '10192', 'model' : 'onoff'},
            { 'id' : '10193', 'model' : 'onoff'},
            { 'id' : '10194', 'model' : 'onoff'},
            { 'id' : '10195', 'model' : 'onoff'},
            { 'id' : '10196', 'model' : 'onoff'},
            { 'id' : '10197', 'model' : 'onoff'},
            { 'id' : '10198', 'model' : 'onoff'},
            { 'id' : '10199', 'model' : 'onoff'},
            { 'id' : '10208', 'model' : 'onoff'},
            { 'id' : '10209', 'model' : 'onoff'},
            { 'id' : '10210', 'model' : 'onoff'},
            { 'id' : '10211', 'model' : 'onoff'},
            { 'id' : '10212', 'model' : 'onoff'},
            { 'id' : '10213', 'model' : 'onoff'},
            { 'id' : '10214', 'model' : 'onoff'},
            { 'id' : '10215', 'model' : 'onoff'},
            { 'id' : '10224', 'model' : 'onoff'},
            { 'id' : '10225', 'model' : 'onoff'},
            { 'id' : '10226', 'model' : 'onoff'},
            { 'id' : '10227', 'model' : 'onoff'},
            { 'id' : '10228', 'model' : 'onoff'},
            { 'id' : '10229', 'model' : 'onoff'},
            { 'id' : '10230', 'model' : 'onoff'},
            { 'id' : '10231', 'model' : 'onoff'},
            { 'id' : '10240', 'model' : 'onoff'},
            { 'id' : '10241', 'model' : 'onoff'},
            { 'id' : '10242', 'model' : 'onoff'},
            { 'id' : '10243', 'model' : 'onoff'},
            { 'id' : '10244', 'model' : 'onoff'},
            { 'id' : '10245', 'model' : 'onoff'},
            { 'id' : '10246', 'model' : 'onoff'},
            { 'id' : '10247', 'model' : 'onoff'},
            { 'id' : '10256', 'model' : 'onoff'},
            { 'id' : '10257', 'model' : 'onoff'},
            { 'id' : '10258', 'model' : 'onoff'},
            { 'id' : '10259', 'model' : 'onoff'},
            { 'id' : '10260', 'model' : 'onoff'},
            { 'id' : '10261', 'model' : 'onoff'},
            { 'id' : '10262', 'model' : 'onoff'},
            { 'id' : '10263', 'model' : 'onoff'},
            { 'id' : '10272', 'model' : 'onoff'},
            { 'id' : '10273', 'model' : 'onoff'},
            { 'id' : '10274', 'model' : 'onoff'},
            { 'id' : '10275', 'model' : 'onoff'},
            { 'id' : '10276', 'model' : 'onoff'},
            { 'id' : '10277', 'model' : 'onoff'},
            { 'id' : '10278', 'model' : 'onoff'},
            { 'id' : '10279', 'model' : 'onoff'},
            { 'id' : '10288', 'model' : 'onoff'},
            { 'id' : '10289', 'model' : 'onoff'},
            { 'id' : '10290', 'model' : 'onoff'},
            { 'id' : '10291', 'model' : 'onoff'},
            { 'id' : '10292', 'model' : 'onoff'},
            { 'id' : '10293', 'model' : 'onoff'},
            { 'id' : '10294', 'model' : 'onoff'},
            { 'id' : '10295', 'model' : 'onoff'},
            { 'id' : '10304', 'model' : 'onoff'},
            { 'id' : '10305', 'model' : 'onoff'},
            { 'id' : '10306', 'model' : 'onoff'},
            { 'id' : '10307', 'model' : 'onoff'},
            { 'id' : '10308', 'model' : 'onoff'},
            { 'id' : '10309', 'model' : 'onoff'},
            { 'id' : '10310', 'model' : 'onoff'},
            { 'id' : '10311', 'model' : 'onoff'},
            { 'id' : '10320', 'model' : 'onoff'},
            { 'id' : '10321', 'model' : 'onoff'},
            { 'id' : '10322', 'model' : 'onoff'},
            { 'id' : '10323', 'model' : 'onoff'},
            { 'id' : '10324', 'model' : 'onoff'},
            { 'id' : '10325', 'model' : 'onoff'},
            { 'id' : '10326', 'model' : 'onoff'},
            { 'id' : '10327', 'model' : 'onoff'},
            { 'id' : '10336', 'model' : 'onoff'},
            { 'id' : '10337', 'model' : 'onoff'},
            { 'id' : '10338', 'model' : 'onoff'},
            { 'id' : '10339', 'model' : 'onoff'},
            { 'id' : '10340', 'model' : 'onoff'},
            { 'id' : '10341', 'model' : 'onoff'},
            { 'id' : '10342', 'model' : 'onoff'},
            { 'id' : '10343', 'model' : 'onoff'},
            { 'id' : '16200', 'model' : 'onoff'},
            { 'id' : '16201', 'model' : 'onoff'},
            { 'id' : '16202', 'model' : 'onoff'},
            { 'id' : '16203', 'model' : 'onoff'},
            { 'id' : '16204', 'model' : 'onoff'},
            { 'id' : '16205', 'model' : 'onoff'},
            { 'id' : '16206', 'model' : 'onoff'},
            { 'id' : '16207', 'model' : 'onoff'},
            { 'id' : '16216', 'model' : 'onoff'},
            { 'id' : '16217', 'model' : 'onoff'},
            { 'id' : '16218', 'model' : 'onoff'},
            { 'id' : '16219', 'model' : 'onoff'},
            { 'id' : '16220', 'model' : 'onoff'},
            { 'id' : '16221', 'model' : 'onoff'},
            { 'id' : '16222', 'model' : 'onoff'},
            { 'id' : '16223', 'model' : 'onoff'},
            { 'id' : '16232', 'model' : 'onoff'},
            { 'id' : '16233', 'model' : 'onoff'},
            { 'id' : '16234', 'model' : 'onoff'},
            { 'id' : '16235', 'model' : 'onoff'},
            { 'id' : '16236', 'model' : 'onoff'},
            { 'id' : '16237', 'model' : 'onoff'},
            { 'id' : '16238', 'model' : 'onoff'},
            { 'id' : '16239', 'model' : 'onoff'},
            { 'id' : '16248', 'model' : 'onoff'},
            { 'id' : '16249', 'model' : 'onoff'},
            { 'id' : '16250', 'model' : 'onoff'},
            { 'id' : '16251', 'model' : 'onoff'},
            { 'id' : '16252', 'model' : 'onoff'},
            { 'id' : '16253', 'model' : 'onoff'},
            { 'id' : '16254', 'model' : 'onoff'},
            { 'id' : '16255', 'model' : 'onoff'},
            { 'id' : '16264', 'model' : 'onoff'},
            { 'id' : '16265', 'model' : 'onoff'},
            { 'id' : '16266', 'model' : 'onoff'},
            { 'id' : '16267', 'model' : 'onoff'},
            { 'id' : '16268', 'model' : 'onoff'},
            { 'id' : '16269', 'model' : 'onoff'},
            { 'id' : '16270', 'model' : 'onoff'},
            { 'id' : '16271', 'model' : 'onoff'}
        ];

    def set_config(self, config):
        try:
            new_config = copy.copy(config)
            new_config['id'] = self.parent.id + '-TC-' + config['id']

            thingplus.Device.set_config(self, new_config)
        except Exception as error:
            print(self.__class__.__name__, error)


class   TurboBlower(thingplus.Device):
    def __init__(self, parent = None):
        thingplus.Device.__init__(self, parent)
        self.sensor_models = {
            'temperature' : Temperature,
            'pressure' : Pressure,
            'current' : Current,
            'vibration' : Vibration,
            'percent' : Percent,
            'number' : Number,
            'onoff' : OnOff
        }
        self.predefined_sensors = [
            { 'id' : '36000', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36001', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36002', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36003', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36004', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36005', 'model' : 'percent', 'min' : 0, 'max' : 1000, 'scale' : 0.1},
            { 'id' : '36006', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36007', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36008', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36009', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36010', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36011', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36012', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36013', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36014', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36015', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36016', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36017', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '36018', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36019', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36020', 'model' : 'current', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36021', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '36022', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36023', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36024', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '36025', 'model' : 'number', 'min' : 0, 'max' : 1000, 'scale' : 0.1},
            { 'id' : '36026', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36027', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36028', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36029', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36030', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36031', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36032', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36033', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36034', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '36035', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '46100', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46101', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46102', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46103', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46104', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46105', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46106', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46107', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46108', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46109', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46110', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46111', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46112', 'model' : 'temperature', 'min' : -1000, 'max' : 5000, 'scale' : 0.1},
            { 'id' : '46113', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46114', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46115', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46116', 'model' : 'pressure', 'min' : 0, 'max' : 10000, 'scale' : 0.01},
            { 'id' : '46117', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '46118', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '46119', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '46120', 'model' : 'vibration', 'min' : 0, 'max' : 10000, 'scale' : 0.1},
            { 'id' : '46121', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '46122', 'model' : 'number', 'min' : 0, 'max' : 65535, 'scale' : 1},
            { 'id' : '10080', 'model' : 'onoff'},
            { 'id' : '10081', 'model' : 'onoff'},
            { 'id' : '10082', 'model' : 'onoff'},
            { 'id' : '10083', 'model' : 'onoff'},
            { 'id' : '10084', 'model' : 'onoff'},
            { 'id' : '10085', 'model' : 'onoff'},
            { 'id' : '10086', 'model' : 'onoff'},
            { 'id' : '10087', 'model' : 'onoff'},
            { 'id' : '10096', 'model' : 'onoff'},
            { 'id' : '10097', 'model' : 'onoff'},
            { 'id' : '10098', 'model' : 'onoff'},
            { 'id' : '10099', 'model' : 'onoff'},
            { 'id' : '10100', 'model' : 'onoff'},
            { 'id' : '10101', 'model' : 'onoff'},
            { 'id' : '10102', 'model' : 'onoff'},
            { 'id' : '10112', 'model' : 'onoff'},
            { 'id' : '10113', 'model' : 'onoff'},
            { 'id' : '10114', 'model' : 'onoff'},
            { 'id' : '10115', 'model' : 'onoff'},
            { 'id' : '10116', 'model' : 'onoff'},
            { 'id' : '10117', 'model' : 'onoff'},
            { 'id' : '10118', 'model' : 'onoff'},
            { 'id' : '10119', 'model' : 'onoff'},
            { 'id' : '10128', 'model' : 'onoff'},
            { 'id' : '10129', 'model' : 'onoff'},
            { 'id' : '10130', 'model' : 'onoff'},
            { 'id' : '10131', 'model' : 'onoff'},
            { 'id' : '10132', 'model' : 'onoff'},
            { 'id' : '10133', 'model' : 'onoff'},
            { 'id' : '10134', 'model' : 'onoff'},
            { 'id' : '10135', 'model' : 'onoff'},
            { 'id' : '10144', 'model' : 'onoff'},
            { 'id' : '10145', 'model' : 'onoff'},
            { 'id' : '10146', 'model' : 'onoff'},
            { 'id' : '10147', 'model' : 'onoff'},
            { 'id' : '10148', 'model' : 'onoff'},
            { 'id' : '10149', 'model' : 'onoff'},
            { 'id' : '10150', 'model' : 'onoff'},
            { 'id' : '10151', 'model' : 'onoff'},
            { 'id' : '10160', 'model' : 'onoff'},
            { 'id' : '10161', 'model' : 'onoff'},
            { 'id' : '10162', 'model' : 'onoff'},
            { 'id' : '10163', 'model' : 'onoff'},
            { 'id' : '10164', 'model' : 'onoff'},
            { 'id' : '10165', 'model' : 'onoff'},
            { 'id' : '10166', 'model' : 'onoff'},
            { 'id' : '10167', 'model' : 'onoff'},
            { 'id' : '10176', 'model' : 'onoff'},
            { 'id' : '10177', 'model' : 'onoff'},
            { 'id' : '10178', 'model' : 'onoff'},
            { 'id' : '10179', 'model' : 'onoff'},
            { 'id' : '10180', 'model' : 'onoff'},
            { 'id' : '10181', 'model' : 'onoff'},
            { 'id' : '10182', 'model' : 'onoff'},
            { 'id' : '10183', 'model' : 'onoff'},
            { 'id' : '10192', 'model' : 'onoff'},
            { 'id' : '10193', 'model' : 'onoff'},
            { 'id' : '10194', 'model' : 'onoff'},
            { 'id' : '10195', 'model' : 'onoff'},
            { 'id' : '10196', 'model' : 'onoff'},
            { 'id' : '10197', 'model' : 'onoff'},
            { 'id' : '10198', 'model' : 'onoff'},
            { 'id' : '10199', 'model' : 'onoff'},
            { 'id' : '10208', 'model' : 'onoff'},
            { 'id' : '10209', 'model' : 'onoff'},
            { 'id' : '10210', 'model' : 'onoff'},
            { 'id' : '10211', 'model' : 'onoff'},
            { 'id' : '10212', 'model' : 'onoff'},
            { 'id' : '10213', 'model' : 'onoff'},
            { 'id' : '10214', 'model' : 'onoff'},
            { 'id' : '10215', 'model' : 'onoff'},
            { 'id' : '10224', 'model' : 'onoff'},
            { 'id' : '10225', 'model' : 'onoff'},
            { 'id' : '10226', 'model' : 'onoff'},
            { 'id' : '10227', 'model' : 'onoff'},
            { 'id' : '10228', 'model' : 'onoff'},
            { 'id' : '10229', 'model' : 'onoff'},
            { 'id' : '10230', 'model' : 'onoff'},
            { 'id' : '10231', 'model' : 'onoff'},
            { 'id' : '10240', 'model' : 'onoff'},
            { 'id' : '10241', 'model' : 'onoff'},
            { 'id' : '10242', 'model' : 'onoff'},
            { 'id' : '10243', 'model' : 'onoff'},
            { 'id' : '10244', 'model' : 'onoff'},
            { 'id' : '10245', 'model' : 'onoff'},
            { 'id' : '10246', 'model' : 'onoff'},
            { 'id' : '10247', 'model' : 'onoff'},
            { 'id' : '10256', 'model' : 'onoff'},
            { 'id' : '10257', 'model' : 'onoff'},
            { 'id' : '10258', 'model' : 'onoff'},
            { 'id' : '10259', 'model' : 'onoff'},
            { 'id' : '10260', 'model' : 'onoff'},
            { 'id' : '10261', 'model' : 'onoff'},
            { 'id' : '10262', 'model' : 'onoff'},
            { 'id' : '10263', 'model' : 'onoff'},
            { 'id' : '10272', 'model' : 'onoff'},
            { 'id' : '10273', 'model' : 'onoff'},
            { 'id' : '10274', 'model' : 'onoff'},
            { 'id' : '10275', 'model' : 'onoff'},
            { 'id' : '10276', 'model' : 'onoff'},
            { 'id' : '10277', 'model' : 'onoff'},
            { 'id' : '10278', 'model' : 'onoff'},
            { 'id' : '10279', 'model' : 'onoff'},
            { 'id' : '10288', 'model' : 'onoff'},
            { 'id' : '10289', 'model' : 'onoff'},
            { 'id' : '10290', 'model' : 'onoff'},
            { 'id' : '10291', 'model' : 'onoff'},
            { 'id' : '10292', 'model' : 'onoff'},
            { 'id' : '10293', 'model' : 'onoff'},
            { 'id' : '10294', 'model' : 'onoff'},
            { 'id' : '10295', 'model' : 'onoff'},
            { 'id' : '10304', 'model' : 'onoff'},
            { 'id' : '10305', 'model' : 'onoff'},
            { 'id' : '10306', 'model' : 'onoff'},
            { 'id' : '10307', 'model' : 'onoff'},
            { 'id' : '10308', 'model' : 'onoff'},
            { 'id' : '10309', 'model' : 'onoff'},
            { 'id' : '10310', 'model' : 'onoff'},
            { 'id' : '10311', 'model' : 'onoff'},
            { 'id' : '10320', 'model' : 'onoff'},
            { 'id' : '10321', 'model' : 'onoff'},
            { 'id' : '10322', 'model' : 'onoff'},
            { 'id' : '10323', 'model' : 'onoff'},
            { 'id' : '10324', 'model' : 'onoff'},
            { 'id' : '10325', 'model' : 'onoff'},
            { 'id' : '10326', 'model' : 'onoff'},
            { 'id' : '10327', 'model' : 'onoff'},
            { 'id' : '10336', 'model' : 'onoff'},
            { 'id' : '10337', 'model' : 'onoff'},
            { 'id' : '10338', 'model' : 'onoff'},
            { 'id' : '10339', 'model' : 'onoff'},
            { 'id' : '10340', 'model' : 'onoff'},
            { 'id' : '10341', 'model' : 'onoff'},
            { 'id' : '10342', 'model' : 'onoff'},
            { 'id' : '10343', 'model' : 'onoff'},
            { 'id' : '16200', 'model' : 'onoff'},
            { 'id' : '16201', 'model' : 'onoff'},
            { 'id' : '16202', 'model' : 'onoff'},
            { 'id' : '16203', 'model' : 'onoff'},
            { 'id' : '16204', 'model' : 'onoff'},
            { 'id' : '16205', 'model' : 'onoff'},
            { 'id' : '16206', 'model' : 'onoff'},
            { 'id' : '16207', 'model' : 'onoff'},
            { 'id' : '16216', 'model' : 'onoff'},
            { 'id' : '16217', 'model' : 'onoff'},
            { 'id' : '16218', 'model' : 'onoff'},
            { 'id' : '16219', 'model' : 'onoff'},
            { 'id' : '16220', 'model' : 'onoff'},
            { 'id' : '16221', 'model' : 'onoff'},
            { 'id' : '16222', 'model' : 'onoff'},
            { 'id' : '16223', 'model' : 'onoff'},
            { 'id' : '16232', 'model' : 'onoff'},
            { 'id' : '16233', 'model' : 'onoff'},
            { 'id' : '16234', 'model' : 'onoff'},
            { 'id' : '16235', 'model' : 'onoff'},
            { 'id' : '16236', 'model' : 'onoff'},
            { 'id' : '16237', 'model' : 'onoff'},
            { 'id' : '16238', 'model' : 'onoff'},
            { 'id' : '16239', 'model' : 'onoff'},
            { 'id' : '16248', 'model' : 'onoff'},
            { 'id' : '16249', 'model' : 'onoff'},
            { 'id' : '16250', 'model' : 'onoff'},
            { 'id' : '16251', 'model' : 'onoff'},
            { 'id' : '16252', 'model' : 'onoff'},
            { 'id' : '16253', 'model' : 'onoff'},
            { 'id' : '16254', 'model' : 'onoff'},
            { 'id' : '16255', 'model' : 'onoff'},
            { 'id' : '16264', 'model' : 'onoff'},
            { 'id' : '16265', 'model' : 'onoff'},
            { 'id' : '16266', 'model' : 'onoff'},
            { 'id' : '16267', 'model' : 'onoff'},
            { 'id' : '16268', 'model' : 'onoff'},
            { 'id' : '16269', 'model' : 'onoff'},
            { 'id' : '16270', 'model' : 'onoff'},
            { 'id' : '16271', 'model' : 'onoff'}
        ];

    def set_config(self, config):
        try:
            new_config = copy.copy(config)
            new_config['id'] = self.parent.id + '-BL-' + config['id']

            thingplus.Device.set_config(self, new_config)
        except Exception as error:
            print(self.__class__.__name__, error)

class   Sensor(thingplus.Sensor):
    def __init__(self, parent = None):
        thingplus.Sensor.__init__(self, parent)
        self.simulation = True
        self.direction = 1

    def set_config(self, config):
        try:
            new_config = copy.copy(config)
            new_config['id'] = self.parent.id + '-' + config['id']

            thingplus.Sensor.set_config(self, new_config)
        except Exception as error:
            print(self.__class__.__name__, error)


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
        #print('{0:s} : {1:s}, {2:s}'.format(self.id, str(self.time), str(self.value)))

class   Temperature(Sensor):
    def __init__(self, parent = None):
        Sensor.__init__(self, parent)
        self.type = 'temperature'
        self.min = 0
        self.max = 100
        self.scale = 1
        self.unit = 'C'

class   Current(Sensor):
    def __init__(self, parent = None):
        Sensor.__init__(self, parent)
        self.type = 'current'
        self.min = 0
        self.max = 100
        self.scale = 1
        self.unit = 'A'


class   Pressure(Sensor):
    def __init__(self, parent = None):
        Sensor.__init__(self, parent)
        self.type = 'pressure'
        self.min = 0
        self.max = 10000
        self.scale = 1
        self.unit = 'kg/cm2'

class   Vibration(Sensor):
    def __init__(self, parent = None):
        Sensor.__init__(self, parent)
        self.type = 'vibration'
        self.min = 0
        self.max = 10000
        self.scale = 1
        self.unit = ''

class   Percent(Sensor):
    def __init__(self, parent = None):
        Sensor.__init__(self, parent)
        self.type = 'percent'
        self.min = 0
        self.max = 1000
        self.scale = 0.1
        self.unit = ''

class   Number(Sensor):
    def __init__(self, parent = None):
        Sensor.__init__(self, parent)
        self.type = 'number'
        self.min = 0
        self.max = 1000
        self.scale = 0.1
        self.unit = ''

class   OnOff(Sensor):
    def __init__(self, parent = None):
        Sensor.__init__(self, parent)
        self.type = 'onoff'
        self.min = 0
        self.max = 1
        self.scale = 1