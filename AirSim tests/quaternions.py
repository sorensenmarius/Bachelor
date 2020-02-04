import setup_path 
import airsim
import time
import math

import numpy

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

print("Taking off")
client.takeoffAsync().join()

client.moveToPositionAsync(1, 1, -1, 5).join()

for i in range(1, 150):
    data = client.getLidarData()
    client.moveByVelocityZAsync(0, 0, -1, 1, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 22.5))
    q = data.pose.orientation
    _, _, yaw = airsim.to_eularian_angles(data.pose.orientation)
    print(math.degrees(yaw))    
    time.sleep(0.1)


def parse_lidarData(self, data):
    # reshape array of floats to array of [X,Y,Z]
    points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
    points = numpy.reshape(points, (int(points.shape[0]/3), 3))
    
    return points