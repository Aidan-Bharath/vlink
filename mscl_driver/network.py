#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import mscl

def create_network(node, basestation, *args, **kwds):
    """
    Convenience function used to construct a network object, apply
    node configuration to all nodes and begin sampling


    args:
        node: mscl object,
            - mscl connected node, node must already be configured
            for Sync Sampling before adding
        basestation: Connection basestation for MSCL node
            - base used to connect the associated node

    kwds: 
        network_check: Bool 
            - checks network status and usage
            - sets return value 
                - return tuple(2,)

        network_lossless: Bool
            - configures network as loosless

    """
    check = kwds["network_check"] if "network_check" in kwds else None
    lossless = kwds["network_lossless"] if "network_lossless" in kwds else None


    try:
        net = mscl.SyncSamplingNetwork(basestation)
        net.addNode(node)

        if check: 
            ret = (net.ok(), net.percentBandwidth())
        if lossless:
            net.lossless(lossless)

        net.applyConfiguration()
        net.startSapling()

    except (AttributeError,ValueError) as e:
        print(e, ' Failed to start network - Exitting')
        if not kwds['debug']: sys.exit() # comment out to conitue execution






if __name__ == "__main__":
    pass
