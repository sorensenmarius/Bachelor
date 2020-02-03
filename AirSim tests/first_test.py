import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

state = client.getMultirotorState()
s = pprint.pformat(state)
print("state: %s" % s)

airsim.wait_key('Press any key to takeoff')
client.takeoffAsync().join()

client.moveToPositionAsync(-5, -5, -5, 10).join();
client.moveToPositionAsync(-10, -5, -10, 10).join();
client.moveToPositionAsync(-10, -10, -10, 10).join();
client.moveToPositionAsync(-10, -10, -1, 10).join();