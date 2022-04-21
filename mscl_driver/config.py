#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, json


def get_config(*args,**kwds):
    """
    Convenience function to open and pull values from
    the config.json file associated with this scripts.

    If no path is passed the function will look in the root dir

    args:
        args[:]: list (iterable)
            - keys of data to be pulled from the config.json

    kwds:
        path: str
            - path to config.json 

    """
    
    if kwds["_p"]:
        _p = str(kwds['_p'])
    else:
        _p = str(os.getcwd())

    config = str(_p)+"/config.json"
    assert os.path.isfile(config), "Config file not found in "+str(_p)

    with open(config,'r') as cf:
        js = json.load(cf)
        try: 
            return [js[arg] for arg in args] 
        except KeyError as e:
            print(e, " - Not found in config.json: Cancel Execution")
            sys.exit()



if __name__ == "__main__":
    pass 
