import setup_path 
import airsim
import math
import time

import utilities as utils
import lidarUtils
import argumentParser as parsing

import numpy as np



class ObstacleAvoidance:
    def __init__(self):
        """ Setup connection tot AirSim and parsing args"""
        self.args = parsing.parseCLIargs()
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
        self.iteration = 0

        if self.args.followPath:
            # List of airsim.Vector3r to follow
            self.path = utils.loadPath(filename = self.args.path)
            self.pathIterator = 0
            self.goal = self.path[self.pathIterator]
        else:
            self.goal = airsim.Vector3r(self.args.points[0], self.args.points[1], self.args.points[2])    
    
        if self.args.saveImageFolder != None:
            self.imageFolderName = utils.setImageFoldername(self.args.saveImageFolder)
        else:
            self.imageFolderName = utils.setImageFoldername()

        self.imageNumber = 0
        self.imageFrequency = 3
        self.lastImageTime = time.thread_time()

    def execute(self):
        """ Main control and high-level logic """
        while self.running:
            self.getImageData()
            self.splitImageData()
            self.updateDronePose()
            self.avoid()
            self.updateGoal()
            # Thought this was the part that was responsible for saving lidar data
            # Made the variable initialized in init decide if the program saves LidaData
            if self.args.sl:
                lidarUtils.handleLidarData(self.client, filename="lidardata")
            if self.args.savePos or self.args.savePosFile:
                if self.args.savePosFile:
                    utils.savePositionToFile(self.client, filename=self.args.savePosFile)
                else:
                    utils.savePositionToFile(self.client, filename="dronePos")
            if self.args.saveImage:
                if(time.thread_time() - self.lastImageTime > self.imageFrequency):
                    self.saveImage()
                    self.imageNumber += 1
                    self.lastImageTime = time.thread_time()
            self.iteration += 1
        print("Ended")

    def avoid(self):
        """ Main collision avoidance logic """
        if self.calculateTooClosePercentage(self.middle) > self.percentage:
            if self.calculateTooClosePercentage(self.left) > self.calculateTooClosePercentage(self.right):
                self.turnRight()
            else:
                self.turnLeft()
        else:
            self.turnTowardsGoal()
    

    def getImageData(self):
        """
            Sets the depth data to the formated matrix
            Values in the matrix are meters from the camera
        """
        responses = self.client.simGetImages([airsim.ImageRequest(0, airsim.ImageType.DepthVis, True)])
        result = responses[0]
        depth = np.array(result.image_data_float, dtype=np.float32)
        for i in range(len(depth)):
            if depth[i] > 1: depth[i] = 1

            depth[i] *= 100
        depth = depth.reshape(result.height, result.width)
        self.depth = depth
    
    def splitImageData(self):
        """ Splits the image data in 3 matrices which indicate the three possible moves (left, middle, right) """
        # Split and only consider the middle data
        vsplit = np.array_split(self.depth, 3)[1]
        # 1 indicates what axis to split
        splits = np.array_split(vsplit, 3, 1) 
        self.left = splits[0]
        self.middle = splits[1]
        self.right = splits[2]
    
    def calculateTooClosePercentage(self, m):
        """ Calculates the percentage of pixels in a matrix that is under a threshold """
        counter = 0
        sum = 0
        for y in m:
            for x in y:
                if x < self.threshold:
                    counter += 1
                sum += 1
        return counter / sum * 100

    
    def showImage(self):
        """ Shows a plot of what the drone sees, with rectangles indicating the different segments the drone considers """
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
        """ Sets the pitch, roll and yaw of the drone to the ObejectAvoidance object """
        self.pitch, self.roll, self.yaw = airsim.to_eularian_angles(self.client.simGetVehiclePose().orientation)

    def fly(self, yaw):
        """ Flies toward the given yaw """
        vx = math.cos(yaw)
        vy = math.sin(yaw)
        self.client.moveByVelocityZAsync(
            vx,
            vy,
            -1,
            2,
            airsim.DrivetrainType.ForwardOnly,
            airsim.YawMode(False, 0)
        )
    
        
    def goForward(self):
        """ Flies the drone straight forward """
        # TODO - Scale speed with distance to obstacle
        self.fly(self.yaw)

    def turnRight(self):
        """ Turns the drone to the right by PI/32 radians """
        # TODO - Scale turn degree
        yaw = self.yaw + math.pi / 32
        self.fly(yaw)

    def turnLeft(self):
        """ Turns the drone to the left by PI/32 radians """
        # TODO - Scale turn degree
        yaw = self.yaw - math.pi / 32
        self.fly(yaw)

    def turnTowardsGoal(self):
        """ 
            Turns the drone towards the goal in self.goal
            Checks if it is safe to turn left or right before turning
                Goes straight if turning is not safe
        """
        pos = self.client.simGetVehiclePose().position
        dX = self.goal.x_val - pos.x_val 
        dY = self.goal.y_val - pos.y_val 
        testYaw = math.atan2(dY, dX)
        yaw = self.yaw
        if(testYaw < yaw):
            if(self.calculateTooClosePercentage(self.left) < self.percentage):
                yaw = self.yaw - (self.yaw - testYaw) / 5
        else:
            if(self.calculateTooClosePercentage(self.right) < self.percentage):
                yaw = self.yaw - (self.yaw - testYaw) / 5
        self.fly(yaw)

    def updateGoal(self):
        """ 
            Updates self.goal if the drone is closer than 3 meters to the current goal
            Should be used if the drone is following a path
        """
        if self.client.simGetVehiclePose().position.distance_to(self.goal) < 3:
            if self.pathIterator < len(self.path) - 1:
                self.pathIterator += 1
                print(f'New goal set')
            else:
                self.running = False
            self.goal = self.path[self.pathIterator]
    
    def saveImage(self):
        """
            Gets an image from the client and saves it to the folder specified in self.imageFolderName
        """
        import os
        import airsim
        
        img = self.client.simGetImage("0", airsim.ImageType.Scene)
        # airsim.write_file(os.path.normpath(f'{foldername}/{str(self.imageNumber)}.png'), img)
        with open(f'{self.imageFolderName}/{str(self.imageNumber)}.png', 'wb') as f:
            f.write(img)
        with open(f'{self.imageFolderName}/pos.txt', 'a') as f:
            pos = self.client.simGetVehiclePose().position
            f.write(f'{self.imageNumber} {pos.x_val} {pos.y_val} {pos.z_val}\n')

    def stop(self):
        """ Safely reset and release AirSim control """
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
        