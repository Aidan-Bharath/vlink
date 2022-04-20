#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/usr/share/python3-mscl")

import mscl

from enum import Enum

class sample(Enum):
    MODE        = mscl.WirelessTypes.samplingMode_sync
    RATE        = mscl.WirelessTypes.sampleRate_1Hz
    DURATION    = True
    TIMEOUT     = 7200


class __IDLE_TEST__(Enum):
    SUCCESS     = mscl.SetToIdleStatus.setToIdleResult_success
    CANCELLED   = mscl.SetToIdleStatus.setToIdleResult_canceled
    FAILED      = None #what is a failed value


def create_mscl_node(tcpIP, tcpP, node, *args, **kwds):
    """
    Create the MSCL wireless node

    args:
        tcpIP: str,
            - TCP-IP address for the mscl Connection

        tcpP: int,
            - TCP-IP Port

        node: int,
            - MSCL node number
    """
    
    try:
        conn = mscl.Connection.TcpIp(tcpIP,tcpP)
        base = mscl.BaseStation(conn)
        return mscl.WirelessNode(node,base), base

    except mscl.Error_InvalidTcpServer as e:
        print(e, "- Server Node Cannot be Created - Exitting")
        if not kwds["debug"]  sys.exit() # comment to conitnue running the script

        return None, None

def test_response(node, *args, **kwds):
    """
    Ping the node, to test the connection  
    
    args:
        node: mscl Object,
            - mscl connected node

    kwds:
        pass
    """
    
    try:
        response = node.ping()
        assert response.success(), "Ping to node unsuccessful - Exitting"
    except (AttributeError) as e:
        print(e, ' - Node not available - Exitting')
        if not kwds["debug"]  sys.exit() # comment to conitnue running the script




def set_RSSI(node, *args, **kwds):
    """
    Ping the node, and set RSSI  
    
    args:
        node: mscl Object,
            - mscl connected node

    kwds:
        pass
    """
   
    try:
        response = node.ping()
        response.baseRsst()
        response.nodeRsst()
    except AttributeError as e:
        # pass when node doesn't exist
        print(e, "Failed to set RSSI - Exiting")
        if not kwds["debug"]  sys.exit() # comment to conitnue running the script
    finally:
        return node



def set_idle_status(node, *args, **kwds):
    """
    Get and set the idle status of the node 

    """

    try:
        idleStatus = node.setToIdle()
        while not idleStatus.complete(): #threading?
            print("."),
        result = __IDLE_TEST__(idleStatus.result())
        print(f"Set to Idle returned: {result}")

    except (AttributeError, ValueError) as e:
        print(e, "- Failed Node Set to Idle - Exitting")
        if not kwds["debug"]  sys.exit() # comment to conitnue running the script
    finally:
        return node



def set_node_config(node, *args, **kwds):
    """
    set node configuration

    args:
        node: mscl Object,
            - mscl connected node

    kwds:
        pass

    """
    
    kwds['rate'] = kwds['rate'] if kwds['rate'] else sample.RATE 
    kwds['mode'] = kwds['mode'] if kwds['mode'] else sample.MODE
    kwds['duration'] = kwds['duration'] if kwds['duration'] else sample.DURATION 
    kwds['timeout'] = kwds['timeout'] if kwds['timeout'] else sample.TIMEOUT

    config = mscl.WirelessNodeConfig()

    try:
        config.inactivityTimeout(kwds["timeout"])
        config.sampleingMode(kwds['mode'])
        config.sampleRate(kwds['rate'])
        config.unlimitedDuration(kwds['duration'])
        node.applyConfig(config)

    except AttributeError as e:
        print(e, "- Failed in Node Configure - Exiting")
        if not kwds["debug"]  sys.exit() # comment to conitnue running the script

    finally:
        return node


def show_node_config(node,*args,**kwds): 
    """
    Convenience function to print the relevent parameters
    one might wnat to see

    args:
        node: mscl Object,
            - mscl connected node

    kwds:
        pass
    """
    
    debug = kwds["debug"] if "debug" in kwds else None

    try:
        if debug: 
            log = 'test' 
            timeout = 'test'
            channels = 'test'
            sweeps = 'test'
        else:
            log = node.getNumDatalogSessions
            timeout = node.getInactivityTimeout()
            channels = node.getActiveChannels()
            sweeps = node.getNumSweeps()

        cases = f"""
        Node Configuration Parameters: 

                Number of Data Log Sessions: {log} 
                Inactivity Timeout: {timeout} 
                Number of Active Channels: {channels} 
                Number of Sweeps: {sweeps} 
                """ 
        print(cases)

    except (AttributeError) as e:
        print(e, ' - Node not available - Exitting')
        if not kwds["debug"]  sys.exit() # comment to conitnue running the script




if __name__ == "__main__":
    pass
