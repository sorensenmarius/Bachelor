import setup_path 
import airsim

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

print("Taking off")
client.takeoffAsync(timeout_sec=5).join()

client.moveToPositionAsync(0, 0, -10, 3).join()


client.moveToPositionAsync(0, -50, -10, 3).join()

client.moveToPositionAsync(0, -50, -1, 3).join()

client.goHomeAsync().join()