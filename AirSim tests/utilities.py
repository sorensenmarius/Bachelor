import matplotlib.pyplot as plt

def showMatrix(m):
    fig = plt.figure()
    plt.imshow(m)
    plt.colorbar()
    plt.show()

def savePositionToFile(client, foldername="droneData", filename="position"):
    """Gets the position of the drone and saves it to the specified file in the specified folder"""
    
    pos = client.simGetVehiclePose().position
    with open(f'{foldername}/{filename}.txt', 'a') as f:
        f.write(f'{pos.x_val},{pos.y_val},{pos.z_val}\n')