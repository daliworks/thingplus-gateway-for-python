#!/usr/local/bin/python3

import sys 
import getopt
import thingplus
import json


def main(argv):
    try:
        opts,args = getopt.getopt(argv, 'c:')
    except getopt.GetoptError as err:
        print('app.py -c <configfile> : ' + err.message)
        sys.exit(2)

    config = None
    for opt,arg in opts:
        if opt == '-c':
            json_data=open(arg).read() 
            config = json.loads(json_data)

    client = thingplus.Client(config)
    client.print()

    client.start()

if __name__ == "__main__":
   main(sys.argv[1:])