import setup_path 
import airsim
import math
import time

import utilities as utils

import numpy as np

class ObstacleAvoidance:
    # Setup connection to AirSim
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)        
        self.client.takeoffAsync().join()



        # Variables

        # Shorter distance = too close
        self.threshold = 5
        # Percentage of middle pixels that need to be too close to turn
        self.percentage = 20
        # Time to wait each step in seconds
        self.waitTime = 0.5
        self.running = True

        # The goal the drone is trying to reach
        self.goal = airsim.Vector3r(-200, 0, -2)

    # Main control of high-level logic
    def execute(self):
        # Get and format image data
        # Split image data in 3 parts
        # Check if middle part is too close
        # if(middleTooClose)
        #   Check right and left
        #   Turn
        # else
        #   Go straight
        while self.running:
            self.getImageData()
            self.splitImageData()
            self.updateDronePose()
            self.avoid()
            time.sleep(self.waitTime)

    # Main collision avoidance logic
    def avoid(self):
        if self.calculateTooClosePercentage(self.middle) > self.percentage:
            if self.calculateTooClosePercentage(self.left) > self.calculateTooClosePercentage(self.right):
                self.turnRight()
            else:
                self.turnLeft()
        else:
            # TODO - Turn towards finish point if possible
            # self.goForward()
            self.turnTowardsGoal()
    
    # Sets the depth data to the formated matrix
    # Values in the matrix are meters from the camera (I think :S)
    def getImageData(self):
        responses = self.client.simGetImages([airsim.ImageRequest(0, airsim.ImageType.DepthVis, True)])
        result = responses[0]
        depth = np.array(result.image_data_float, dtype=np.float32)
        for i in range(len(depth)):
            if depth[i] > 1: depth[i] = 1

            # Value 255 = 100 meters range
            # This multiplication converts from 0 - 255 value to approx. meters in range 0 - 100
            depth[i] *= 255 * 0.392157
        depth = depth.reshape(result.height, result.width)
        self.depth = depth
    
    # Splits the image data in 3 matrices which indicate the three possible moves (left, middle, right)
    def splitImageData(self):
        # Split and only consider the middle data
        vsplit = np.array_split(self.depth, 3)[1]
        # 1 indicates what axis to split
        splits = np.array_split(vsplit, 3, 1) 
        self.left = splits[0]
        self.middle = splits[1]
        self.right = splits[2]
    
    # Calculates the percentage of pixels in a matrix that is under a threshold
    def calculateTooClosePercentage(self, m):
        counter = 0
        sum = 0
        for y in m:
            for x in y:
                if x < self.threshold:
                    counter += 1
                sum += 1
        return counter / sum * 100
    
    def showImage(self):
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        # TODO - Fix this so it is not so hacky in calculating x coordinate of middle and right
        left = patches.Rectangle((0, len(self.left)), height = len(self.left), width = len(self.left[0]), fill=False)
        middle = patches.Rectangle((len(self.left[0]), len(self.left)), height = len(self.left), width = len(self.left[0]), fill=False)
        right = patches.Rectangle((len(self.left[0]) * 2, len(self.left)), height = len(self.left), width = len(self.left[0]), fill=False)
        fig,ax = plt.subplots()
        ax.imshow(self.depth)
        # plt.colorbar()
        ax.add_patch(left)
        ax.add_patch(middle)
        ax.add_patch(right)
        plt.show()

    def updateDronePose(self):
        self.pitch, self.roll, self.yaw = airsim.to_eularian_angles(self.client.simGetVehiclePose().orientation)

    # Movement functions
    
    def fly(self, yaw):
        vx = math.cos(yaw)
        vy = math.sin(yaw)
        self.client.moveByVelocityZAsync(
            vx,
            vy,
            -1,
            self.waitTime,
            airsim.DrivetrainType.ForwardOnly,
            airsim.YawMode(False, 0)
        )
    
    # Flies the drone straight forward
    # TODO - Scale speed with distance to obstacle
    def goForward(self):
        self.fly(self.yaw)

    # Turns the drone to the right
    # TODO - Scale turn degree
    def turnRight(self):
        yaw = self.yaw + math.pi / 8
        self.fly(yaw)

    # Turns the drone to the left
    # TODO - Scale turn degree
    def turnLeft(self):
        yaw = self.yaw - math.pi / 8
        self.fly(yaw)

    # Checks if the drone can turn towards the goal
    # TODO - Scale how much it turns
    #   Maybe use % of what way we are turning to scale
    def turnTowardsGoal(self):
        pos = self.client.simGetVehiclePose().position
        dX = pos.x_val - self.goal.x_val
        dY = pos.y_val - self.goal.y_val
        testYaw = math.atan2(dY, dX)
        yaw = self.yaw
        if(yaw > 0):
            if(self.calculateTooClosePercentage(self.left) < self.percentage):
                yaw = self.yaw - (self.yaw - testYaw) / 5
        else:
            if(self.calculateTooClosePercentage(self.right) < self.percentage):
                yaw = self.yaw - (self.yaw - testYaw) / 5
        self.fly(yaw)

    # Safely reset and release AirSim control
    def stop(self):
        airsim.wait_key('Press any key to reset to original state')
        self.client.armDisarm(False)
        self.client.reset()
        self.client.enableApiControl(False)
        print("Done!\n")

# main
if __name__ == "__main__":
    avoid = ObstacleAvoidance()
    try:
        avoid.execute()
    finally:
        avoid.stop()
        