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
client.moveToPositionAsync(0, 0, -1, 2).join()

v = 1
# for i in range(1, 100):
while True:
    data = client.getDistanceSensorData(distance_sensor_name="DistF", vehicle_name="Drone")
    print("Distance: " + str(data.distance))
    _, _, yaw  = airsim.to_eularian_angles(client.simGetVehiclePose().orientation)
    vx = math.cos(yaw) * v
    vy = math.sin(yaw) * v
    print("vx: " + str(vx) + ", vy: " + str(vy) + ", yaw: " + str(yaw))
    if(data.distance < 9):
        client.moveByVelocityZAsync(vx, vy, -1, 0.2, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, (1/data.distance) * 100))
        print("Turning by: " + str((1/data.distance) * 100))
    else:
        client.moveByVelocityZAsync(vx, vy, -1, 0.2, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(True, 0))
    time.sleep(0.20);