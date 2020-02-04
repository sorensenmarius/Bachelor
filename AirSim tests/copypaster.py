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

# Makes the drone fly and get Lidar data
class LidarTest:

    def __init__(self):

        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def execute(self):

        print("arming the drone...")
        self.client.armDisarm(True)

        state = self.client.getMultirotorState()
        s = pprint.pformat(state)
        #print("state: %s" % s)

        # self.client.takeoffAsync().join()

        state = self.client.getMultirotorState()
        #print("state: %s" % pprint.pformat(state))
        
        # for i in range(1,5):
        #     self.client.moveByVelocityZAsync(0, 0, -1, 5, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 90))
        #     lidarData = self.client.getLidarData();
        #     if (len(lidarData.point_cloud) < 3):
        #         print("\tNo points received from Lidar data")
        #     else:
        #         points = self.parse_lidarData(lidarData)
        #         print(points)
        #         for p in points:
        #             print(lidarData.pose.position.distance_to(airsim.Vector3r(p[0], p[1], p[2])))
        #         print(lidarData.pose.position)
        #     time.sleep(5)

        v = 1
        while True:
            lidarData = self.client.getLidarData()
            if (len(lidarData.point_cloud) < 3):
                print("\tNo points received from Lidar data")
                continue
            
            points = self.parse_lidarData(lidarData)
            distances = []
            pose = self.client.simGetVehiclePose()
            for p in points:
                distances.append((p, pose.position.distance_to(airsim.Vector3r(p[0], p[1], p[2]))))
            distances.sort(key=lambda tup: tup[1])
            _, _, yaw  = airsim.to_eularian_angles(pose.orientation)
            vx = math.cos(yaw) * v
            vy = math.sin(yaw) * v
            d = distances[0][1]
            print(d)
            print(distances[0][1], distances[int(len(distances) / 2)][1], distances[len(distances) - 1][1])
            if(d < 4):
                self.client.moveByVelocityZAsync(vx, vy, -1, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, (1/d) * 100))
                print("Turning right by: " + str((1/d) * 100))
            else:
                self.client.moveByVelocityZAsync(vx, vy, -1, 0.5, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, -(1/d) * 100))
                print("Turning left by: " + str((1/d) * 100))
            time.sleep(1)

    def parse_lidarData(self, data):

        # reshape array of floats to array of [X,Y,Z]
        points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
        points = numpy.reshape(points, (int(points.shape[0]/3), 3))
       
        return points

    def write_lidarData_to_disk(self, points):
        # TODO
        print("not yet implemented")

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

    arg_parser = argparse.ArgumentParser("Lidar.py makes drone fly and gets Lidar data")

    arg_parser.add_argument('-save-to-disk', type=bool, help="save Lidar data to disk", default=False)
  
    args = arg_parser.parse_args(args)    
    lidarTest = LidarTest()
    try:
        lidarTest.execute()
    finally:
        lidarTest.stop()