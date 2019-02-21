#!/usr/local/bin/python3

import sys 
import getopt
import thingplus
from seah import Gateway
import json
import copy


def main(argv):
    try:
        opts,args = getopt.getopt(argv, 'c:')
    except getopt.GetoptError as err:
        print('app.py -c <configfile> : ' + err)
        sys.exit(2)

    print(opts)
    config = None
    for opt,arg in opts:
        if opt == '-c':
            json_data=open(arg).read() 
            config = json.loads(json_data)


    gateway_list = []
    for gateway_config in config['gateways']:
        try:
            def get_server_config(configs, id):
                try:
                    for config in configs:
                        if config.get('id') == id:
                            return  config
                except Exception as error:
                    print(error)

                return  None 

            if gateway_config.get('server') is None:
                server_id = gateway_config.get('server_id')
                if server_id is None:
                    gateway_config['server'] = get_server_config(config.get('servers'), 1)
                else:
                    gateway_config['server'] = get_server_config(config.get('servers'), server_id)

            gateway = Gateway.create(gateway_config)
            gateway_list.append(gateway)
        except Exception as error:
            print(error)

    for gateway in gateway_list:
        gateway.start()

if __name__ == "__main__":
   main(sys.argv[1:])