#!/usr/bin/env python
# -*- coding: utf-8 -*-


from struct import pack


def get_data(basestation, *args, **kwds):

    try:
        sweeps = basestation.getData(kwds["timeout"])

        for sweep in sweeps:
            if kwds["node_address"]: sweep.nodeAddress()
            if kwds["time_stamp"]: sweep.timestamp()
            if kwds["tick"]: sweep.tick()
            if kwds["sample_rate"]: sweep.sampleRate()
            if kwds["sample_type"]: sweep.samplingType()
            if kwds["node_rssi"]: sweep.nodeRssi()
            if kwds["base_rssi"]: sweep.baseRssi()
            if kwds["frequency"]: sweep.frequency()

            for data in sweep.data():
                data.channelName() # why is this here?
                try: 
                    bytesToSend = bytearray(pack("d",data.as_float()))
                except (ValueError) as e:
                    print(e, " - Error in sampled Value")
                    bytesToSend = None



    except (AttributeError) as e:
        print(e, " - Error in sweeping though samples - Exitting")
        if not kwds["debug"]: sys.exit # comment out to continue program
    

    finally:
        
        return data 







if __name__ == "__main__":
    pass
