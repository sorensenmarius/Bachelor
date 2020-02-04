import setup_path 
import airsim

import numpy

class DistanceTest:
    def __init__(self):
        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def execute(self):
        for i in range(1, 10):
            airsim.wait_key("Trykk")
            self.client.moveByVelocityZAsync(0, 0, -1, 1, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 90)).join()
            self.client.moveByVelocityZAsync(0, 0, -1, 1, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 0)).join()
            self.client.hoverAsync()
            self.dist()

        # self.client.moveByVelocityZAsync(0, 0, -1, 5, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 90)).join()
        # self.dist()
        # self.client.moveByVelocityZAsync(0, 0, -1, 5, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 90)).join()
        # self.dist()
        # self.client.moveByVelocityZAsync(0, 0, -1, 5, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 90)).join()
        # self.dist()
        # self.client.moveByVelocityZAsync(0, 0, -1, 5, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 90)).join()

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
        print(distances[0][1], distances[int(len(distances) / 2)][1], distances[len(distances) - 1][1])

    def stop(self):

        airsim.wait_key('Press any key to reset to original state')

        self.client.armDisarm(False)
        self.client.reset()

        self.client.enableApiControl(False)
        print("Done!\n")

# print(client.simGetVehiclePose())
# print(airsim.Vector3r(1, 1, -1).distance_to(client.simGetVehiclePose().position))
# client.moveToPositionAsync(1, 1, -1, 2).join()
# print(client.simGetVehiclePose())
# print(airsim.Vector3r(1, 1, -1).distance_to(client.simGetVehiclePose().position))
# client.moveToPositionAsync(-1, -1, -1, 2).join()
# print(client.simGetVehiclePose())
# print(airsim.Vector3r(1, 1, -1).distance_to(client.simGetVehiclePose().position))
# client.moveToPositionAsync(1, 1, -1, 2).join()
# print(client.simGetVehiclePose())
# print(airsim.Vector3r(1, 1, -1).distance_to(client.simGetVehiclePose().position))

if __name__ == "__main__":
    distanceTest = DistanceTest()
    try:
        distanceTest.execute()
    finally:
        distanceTest.stop()