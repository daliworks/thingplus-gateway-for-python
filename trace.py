import time
import logging
import traceback

class   Trace():
    def __init__(self, object = None):
        self.object = object
        self.time_field = True
        self.level_field = True
        self.name_field = True
        self.id_field = False
        self.level = ['DBG', 'INF', 'ERR']
        self.name =  self.object.__class__.__name__
        self.logger = logging.getLogger(self.name) 
      
        #ch = logging.StreamHandler()
        #ch.setLevel(logging.DEBUG)

        # create formatter
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        #ch.setFormatter(formatter)

        # add ch to logger
        #self.logger.addHandler(ch)

    def debug(self, *args):
        if 'DBG' in self.level:
            output = ''
            for arg in args:
                output = output + ' {0}'.format(arg)
            #logging.debug(output)
            self.logger.debug(output)

    def info(self, *args):
        if 'INF' in self.level:
            output = ''
            for arg in args:
                output = output + ' {0}'.format(arg)
            #logging.info(output)
            self.logger.info(output)

    def error(self, *args):
        if 'ERR' in self.level:
            #traceback.print_stack()
            output = ''
            for arg in args:
                output = output + ' {0}'.format(arg)
            logging.error(output)
            #self.logger.error(output)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
trace_ = Trace()

def debug(*args):
    trace_.debug(*args)
    None

def info(*args):
    trace_.info(*args)
    None

def error(*args):
    trace_.err(*args)
    None
