import time
import traceback

class   Trace():
    def __init__(self, object):
        self.object = object
        self.time_field = True
        self.level_field = True
        self.name_field = True
        self.id_field = False
        self.level = ['DBG', 'INF', 'ERR']
        self.name =  self.object.__class__.__name__

    def header(self, time, level, name):
        output = ''
        if self.time_field:
            output = output + '[{0:d}]'.format(time)

        if self.level_field:
            output = output + '[{0:s}]'.format(level)

        if self.name_field:
            output = output + '[{0:s}]'.format(name)

        if self.id_field:
            if self.object is not None and self.object.id is not None:
                output = output + '[{0:s}]'.format(self.object.id)

        return  output

    def debug(self, first, *args):
        if 'DBG' in self.level:
            print(self.header(int(time.time()), 'DBG', self.name), first, *args)

    def info(self, first, *args):
        if 'INF' in self.level:
            print(self.header(int(time.time()), 'INF', self.name), first, *args)

    def error(self, first, *args):
        if 'ERR' in self.level:
            traceback.print_stack()
            print(self.header(int(time.time()), 'ERR', self.name), first, *args)

def header(self, time, level, name = ''):
    output = ''
    output = output + '[{0:s}]'.format(time)
    output = output + '[{0:s}]'.format(level)
    output = output + '[{0:s}]'.format(name)

    return  output

def debug(first, *args):
    print(header(int(time.time()), 'DBG', 'GLOBAL'), first, *args)

def info(first, *args):
    print(header(int(time.time()), 'INF', 'GLOBAL'), first, *args)

def error(first, *args):
    print(header(int(time.time()), 'ERR', 'GLOBAL'), first, *args)
