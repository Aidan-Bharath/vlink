import sys
sys.path.append('/usr/share/python3-mscl')

import socket
import struct
import mscl
 
serverAddressPort   = ("192.168.0.21", 20001)

bufferSize          = 1024

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


connection = mscl.Connection.TcpIp("192.168.0.169",5000)
basestation = mscl.BaseStation(connection)

node = mscl.WirelessNode(28175, basestation)

response = node.ping()

if response.success():
    response.baseRssi() # the BaseStation RSSI
    response.nodeRssi()

# call the setToIdle function and get the resulting SetToIdleStatus object
idleStatus = node.setToIdle()

# checks if the Set to Idle operation has completed (successfully or with a failure)
while not idleStatus.complete():
    print("."),

# check the result of the Set to Idle operation
result = idleStatus.result()
if result == mscl.SetToIdleStatus.setToIdleResult_success:
    print("Node is now in idle mode.")
elif result == mscl.SetToIdleStatus.setToIdleResult_canceled:
    print("Set to Idle was canceled!")
else:
    print("Set to Idle has failed!")


# get the number of datalogging sessions stored on the node
node.getNumDatalogSessions()

# get the user inactivity timeout in seconds
node.getInactivityTimeout()

# get the ActiveChannels
node.getActiveChannels()

# get the number of sweeps to sample for
node.getNumSweeps()




# create a WirelessNodeConfig which is used to set all node configuration options
config = mscl.WirelessNodeConfig()

# set the configuration options that we want to change
config.inactivityTimeout(7200)
config.samplingMode(mscl.WirelessTypes.samplingMode_sync)
config.sampleRate(mscl.WirelessTypes.sampleRate_1Hz)
config.unlimitedDuration(True)

# apply the configuration to the Node

# create a SyncSamplingNetwork object, giving it the BaseStation that will be the master BaseStation for the network
network = mscl.SyncSamplingNetwork(basestation)

# add a WirelessNode to the network.
# Note: The Node must already be configured for Sync Sampling before adding to the network, or else Error_InvalidNodeConfig will be thrown.
network.addNode(node)

network.ok()                # check if the network status is ok
network.lossless(True)      # enable Lossless for the network
network.percentBandwidth()  # get the total percent of bandwidth of the network

# apply the network configuration to every node in the network
network.applyConfiguration()

# start all the nodes in the network sampling.
network.startSampling()

while True:

    # get all the data sweeps that have been collected, with a timeout of 500 milliseconds
    sweeps = basestation.getData(500)

    for sweep in sweeps:
 #       sweep.nodeAddress()    # the node address the sweep is from
 #       sweep.timestamp()      # the TimeStamp of the sweep
 #       sweep.tick()           # the tick of the sweep (0 - 65535 counter)
 #       sweep.sampleRate()     # the sample rate of the sweep
 #       sweep.samplingType()   # the SamplingType of the sweep (sync, nonsync, burst, etc.)
 #       sweep.nodeRssi()       # the signal strength at the Node
 #       sweep.baseRssi()       # the signal strength at the BaseStation
 #       sweep.frequency()      # the radio frequency this was collected on

        # get the vector of data in the sweep
        data = sweep.data()

        # iterate over each point in the sweep (one point per channel)
        for dataPoint in data:
            dataPoint.channelName()    # the name of the channel for this point
            if dataPoint.storedAs() == 0:       # the ValueType that the data is stored as
                data_in = dataPoint.as_float()       # get the value as a float
                print(data_in)
                #UDPClientSocket.sendto(bytesToSend, serverAddressPort)
                bytesToSend         = bytearray(struct.pack("d", data_in))  

                UDPClientSocket.sendto(bytesToSend, serverAddressPort)


UDPClientSocket.close()
