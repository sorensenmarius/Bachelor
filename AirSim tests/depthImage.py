import setup_path 
import airsim
import math
import time
import os
import cv2
import numpy as np


class depthImage:
    def __init__(self):
        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def getImageData(self):
        responses = self.client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.DepthVis),  #depth visualization image
        airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True), #depth in perspective projection
        airsim.ImageRequest("1", airsim.ImageType.Scene), #scene vision image in png format
        airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])  #scene vision image in uncompressed RGB array
        print('Retrieved images: %d', len(responses))

        i = 0
        for response in responses:
            i += 1
            filename = 'c:/temp/py' + str(i)
            if not os.path.exists('c:/temp/'):
                os.makedirs('c:/temp/')
            if response.pixels_as_float:
                print(1)
                print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
                airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
            elif response.compress: #png format
                print(2)
                print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
                airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
            else: #uncompressed array
                print(3)
                print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
                img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) # get numpy array
                img_rgb = img1d.reshape(response.height, response.width, 3) # reshape array to 3 channel image array H X W X 3
                cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb) # write to png 

    def takeoff(self):
        self.client.moveByVelocityZAsync(0, 0, -1, 0.5).join()

    def execute(self):
        self.takeoff()
        self.getImageData()

    def stop(self):

        airsim.wait_key('Press any key to reset to original state')

        self.client.armDisarm(False)
        self.client.reset()

        self.client.enableApiControl(False)
        print("Done!\n")

if __name__ == "__main__":
    DI = depthImage()
    try:
        DI.execute()
    finally:
        DI.stop()