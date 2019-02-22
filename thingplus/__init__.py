import trace
import thingplus.vendor.postech as postech
import thingplus.vendor.seah as seah

vendors = {
    'postech' : postech,
    'seah' : seah
}

def create_gateway(config):
    gateway = None
    try:
        gateway = vendors[config.get('vendor')].Gateway.create(config)
    except Exception as error:
        trace.error('Invalid config :', config)

    return  gateway
