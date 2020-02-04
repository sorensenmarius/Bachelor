import setup_path 
import airsim
import math
import time

import numpy

class DistanceTest:
    def __init__(self):
        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def execute(self):
        self.client.moveByVelocityZAsync(0, -1.5, -1, 0.5).join()
        time.sleep(0.5)
        while True:
            if(self.client.simGetCollisionInfo().has_collided):
                print("Kollisjon: ")
                print(self.client.simGetCollisionInfo())
                break
            _, _, yaw  = airsim.to_eularian_angles(self.client.getLidarData().pose.orientation)
            d = self.dist()
            v = 1.5
            vx = math.cos(yaw) * v
            vy = math.sin(yaw) * v
            if(d < 6):
                print(f"D was {d}, turning right")
                self.client.moveByVelocityZAsync(vx, vy, -1, 0.1, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 1/d * 200)).join()
            else:
                print(f"D was {d}, turning left")
                self.client.moveByVelocityZAsync(vx, vy, -1, 0.1, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, -1/d * 200)).join()
        
        
        
        self.client.moveByVelocityZAsync(0, -1, -1, 1, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 0)).join()
        self.client.moveByVelocityAsync(0, 0, 0, 2)


    def parse_lidarData(self, data):

        # reshape array of floats to array of [X,Y,Z]
        points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
        points = numpy.reshape(points, (int(points.shape[0]/3), 3))
       
        return points


    def dist(self):
        lidarData = self.client.getLidarData()
        points = self.parse_lidarData(lidarData)
        distances = []
        pose = self.client.simGetVehiclePose()
        for p in points:
            distances.append((p, pose.position.distance_to(airsim.Vector3r(p[0], p[1], p[2]))))
        distances.sort(key=lambda tup: tup[1])
        # print(distances[0][1], distances[int(len(distances) / 2)][1], distances[len(distances) - 1][1])
        return distances[0][1]

    def stop(self):

        airsim.wait_key('Press any key to reset to original state')

        self.client.armDisarm(False)
        self.client.reset()

        self.client.enableApiControl(False)
        print("Done!\n")

if __name__ == "__main__":
    distanceTest = DistanceTest()
    try:
        distanceTest.execute()
    finally:
        distanceTest.stop()