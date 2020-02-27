# Python client example to get Lidar data from a drone
#

import setup_path 
import airsim

import sys
import math
import time
import argparse
import pprint
import numpy
import numpy as np
import os
from PIL import Image

# Makes the drone fly and get Lidar data
class ImageNavigation:

    def __init__(self):

        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def execute(self):
        print("arming the drone...")
        self.client.armDisarm(True)
        state = self.client.getMultirotorState()

        self.client.takeoffAsync().join()
        self.client.moveByVelocityAsync(0, -1, 0, 5)
        self.getImageData()

        self.stop()

    def getImageData(self):
        print("Getting image data")
        filename = "image"
        for i in range(1, 6):
            responses = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthVis, True, False)])
            response = responses[0]

            newImg = np.zeros((response.height, response.width, 4), dtype=np.uint8)

            y = 0
            x = 0
            maxNum = 0
            for num in response.image_data_float:
                iNum = 255 - num 
                num = num * 100
                if iNum < 0:
                    iNum = 0
                if num > 255: 
                    num = 255
                newImg[y][x % response.width] = [0, num, iNum, 255]

                if x % response.width == 0 and x != 0:
                    y += 1
                x += 1
        
            img = Image.fromarray(newImg, 'RGBA')
            img.save("myImage" + str(i) + ".png")

            time.sleep(1)

    def stop(self):
        airsim.wait_key('Press any key to reset to original state')

        self.client.armDisarm(False)
        self.client.reset()

        self.client.enableApiControl(False)
        print("Done!\n")

# main
if __name__ == "__main__":
    args = sys.argv
    args.pop(0)

    arg_parser = argparse.ArgumentParser("imageNavigator.py takes off and take a single picture")

    arg_parser.add_argument('-filename', type=str, dest="filename", help="Image filename", default="image")
  
    args = arg_parser.parse_args(args)    
    IN = ImageNavigation()
    IN.args = args
    try:
        IN.execute()
    finally:
        IN.stop()