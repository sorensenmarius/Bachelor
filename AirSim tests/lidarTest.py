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

def add_to_file(arr):
    s = ""
    for i in range(len(arr)):
        if(i % 3 == 0 and i != 0):
            s += "\n"
        s += str(arr[i]) + " "
    with open("lidar.txt", "a") as file:
        file.write(s);

for i in range(1, 100):
    data = client.getLidarData(lidar_name="Lidar", vehicle_name="Drone")
    # client.moveByVelocityZAsync(0, 0, -1, 0.1, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 22.5))
    add_to_file(data.point_cloud);
    time.sleep(0.1)


def parse_lidarData(self, data):

    # reshape array of floats to array of [X,Y,Z]
    points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
    points = numpy.reshape(points, (int(points.shape[0]/3), 3))
    
    return points