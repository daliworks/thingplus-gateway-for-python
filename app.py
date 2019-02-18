#!/usr/local/bin/python3

import sys 
import getopt
import thingplus
import seah
import json


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

    server = thingplus.Server(config['server'])
    for gateway in config['gateways']:
        try:
            server.attach(seah.Gateway(gateway))
        except Exception as error:
            print(error)

    server.print_config()

    server.start()

if __name__ == "__main__":
   main(sys.argv[1:])