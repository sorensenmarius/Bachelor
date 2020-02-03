import setup_path 
import airsim
import time
import math

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

print("Taking off")
client.takeoffAsync().join()
print("Getting in position")
client.moveToPositionAsync(0, 2, -1, 2).join()

v = 1
# for i in range(1, 100):
for i in range(1, 25):
    distF = client.getDistanceSensorData(distance_sensor_name="DistF", vehicle_name="Drone")
    distL = client.getDistanceSensorData(distance_sensor_name="DistL", vehicle_name="Drone")
    distR = client.getDistanceSensorData(distance_sensor_name="DistR", vehicle_name="Drone")
    # print("Forward: " + str(distF.distance) + ", Right: " + str(distR.distance) + ", Left: " + str(distL.distance))
    print("Forward")
    print(distF)
    print("Left")
    print(distL)
    print("Right")
    print(distR)
    client.moveByVelocityZAsync(0, 0, -1, 1, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 10))
    time.sleep(0.20);