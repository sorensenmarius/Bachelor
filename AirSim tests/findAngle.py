import setup_path 
import airsim
import math

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.takeoffAsync().join()

pos = client.simGetVehiclePose().position
print(pos)
point = airsim.Vector3r(0, 50, -0.14)
print(point)
dX = pos.x_val - point.x_val
dY = pos.y_val - point.y_val

yaw = math.atan2(dY, dX)