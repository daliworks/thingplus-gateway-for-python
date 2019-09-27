#!/usr/bin/python3

import logging
import sys 
import getopt
import json
import copy
import server as Server
import target as Target

def main(argv):
    try:
        opts,args = getopt.getopt(argv, 'c:')
    except getopt.GetoptError as err:
        print('app.py -c <configfile> : ' + err)
        sys.exit(2)

    config = None
    for opt,arg in opts:
        if opt == '-c':
            json_data=open(arg).read() 
            config = json.loads(json_data)

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    if config is None:
        logging.error('Configuration not defined!')
        sys.exit(2)

    server_list = {}
    for server_config in config['servers']:
        server_list[server_config.get('type')] = Server.create(server_config)

    gateway_list = []
    for gateway_config in config['gateways']:
        if gateway_config.get('server') is None:
            print('Invalid config')
            sys.exit(2)

        try:
            server = server_list[gateway_config.get('server')]
            gateway_config['server'] = server.to_dictionary()
            gateway = Target.create_gateway(config['application'], gateway_config)
            if gateway is not None:
                gateway_list.append(gateway)
                server.attach(gateway)
                gateway.attach(server)
            else:
                logging.error('Gateway creation failed :', gateway)

        except Exception as error:
            logging.error('Unknown exception : %s'%error)
            

    for gateway in gateway_list:
        gateway.start()

if __name__ == "__main__":
    sys.path.append('/home/xtra/Projects/thingplus-gateway-for-python/')

    main(sys.argv[1:])
