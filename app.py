#!/usr/local/bin/python3

import sys 
import getopt
import thingplus
import seah
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
            gateway = seah.create_gateway(gateway_config)
            for server_config in config['servers']:
                if server_config['id'] == gateway.server_id:
                    gateway.server = thingplus.Server(server_config)
            gateway_list.append(gateway)
        except Exception as error:
            print(error)

    for gateway in gateway_list:
        gateway.start()

if __name__ == "__main__":
   main(sys.argv[1:])