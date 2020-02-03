import setup_path
import airsim

import numpy as np
import os
import time

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

client.takeoffAsync().join()

for i in range(0, 1000):
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.DepthVis, True, False)])
    response = responses[0]

    # get numpy array
    img1d = np.fromiter(response.image_data_float, dtype=np.float) 

    # reshape array to 4 channel image array H X W X 4
    img_rgba = img1d.reshape(response.height, response.width, 1)  

    # original image is fliped vertically
    img_rgba = np.flipud(img_rgba)

    x = img_rgba[100][128][0]
    print(x)
    time.sleep(0.1)
    if(x > 250):
        client.moveByAngleZAsync(-1, 0, 1, 50, 0.1).join()
    elif x < 250:    
        client.moveByAngleZAsync(-1, 0, 1, -50, 0.1).join()
    else:
        client.moveByAngleZAsync(-1, 0, 1, 0, 0.1).join()
        vx = math.cos()
        client.moveByVelocityZAsync(0, -1)
    

# airsim.write_png(os.path.normpath('./greener.png'), img_rgba) 

airsim.wait_key('Press any key to reset to original state')

client.armDisarm(False)
client.reset()

client.enableApiControl(False)
print("Done!\n")