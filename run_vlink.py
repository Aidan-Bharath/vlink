
from mscl_driver import *


def run(*args, **kwds):
    """
    General Run function for the vLink based on MSCL Python

    args:
        pass

    kwds:
        path: str,
            - Path to config.json file

    """
    debug = kwds["debug"] if "debug" in kwds else None
    _p = kwds['path'] if "path" in kwds else None
    UDP = []


    serverAddressPort = tuple(get_config("server_addr", "server_port", _p=_p))
    bufferSize, = get_config("bufferSize", _p=_p)
    UDP_config, = get_config("UDP", _p=_p) 


    IP,port,num = get_config("client_addr", "client_port", "node_num", _p=_p)
    node, basestation = create_mscl_node(IP, port, num)
    

    if debug: test_response(node, *args, **kwds)


    node = set_RSSI(node, *args, **kwds)
    node = set_idle_status(node, *args, **kwds)
    
    node_config, = get_config("node_config", _p=_p)
    if node_config: kwds.update(node_config)
    node = set_node_config(node, *args, **kwds) 

    show_node_config(node, *args, **kwds)

    create_network(node,basestation, *args, **kwds)

    with socketcontext(*UDP, **UDP_config) as UDPClientSocket:
        while True:
            bytesToSend = get_data(basestation,*args, **kwds)

            UDPSClientSocket.sendto(bytesToSend, ServerAddresPort)


 


if __name__ == "__main__":

    args = []
    kwds = {
            "debug":True,
            "network_check":True,
            "network_lossless":True
            }

    run(*args, **kwds)
