import server.thingplus
import server.shm

def create(target):
    if isinstance(target, str):
        if target == 'thingplus':
            return  server.thingplus.Server()
        elif target == 'shm':
            return  server.shm.Server()
    else:
        if target['type'] == 'thingplus':
            return  server.thingplus.Server(target)
        elif target['type'] == 'shm':
            return  server.shm.Server(target)

    return  None
