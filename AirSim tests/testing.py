import setup_path
import airsim
import math

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(3, 0, 0), airsim.to_quaternion(0, 0, 0)), True)
# airsim.wait_key("Next")

# client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 3, 0), airsim.to_quaternion(0, 0, 0)), True)
# airsim.wait_key("Next")

# client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(-3, 0, 0), airsim.to_quaternion(0, 0, 0)), True)
# airsim.wait_key("Next")

# client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, -3, 0), airsim.to_quaternion(0, 0, 0)), True)
# airsim.wait_key("Next")

points = [
    airsim.Vector3r(5, 0, -1),
    airsim.Vector3r(0, 5, -1),
    airsim.Vector3r(-5, 0, -1),
    airsim.Vector3r(0, -5, -1)
]

client.takeoffAsync().join()

pos = client.simGetVehiclePose().position
dX = points[1].x_val -pos.x_val
dY = points[1].y_val -pos.y_val
yaw = math.atan2(dY, dX)

vx = math.cos(yaw)
vy = math.sin(yaw)

client.moveByVelocityZAsync(
    vx,
    vy,
    -1,
    3,
    airsim.DrivetrainType.ForwardOnly,
    airsim.YawMode(False, 0)
)



airsim.wait_key('Press any key to reset to original state')
client.armDisarm(False)
client.reset()
client.enableApiControl(False)
print("Done!\n")