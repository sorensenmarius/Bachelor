import matplotlib.pyplot as plt
from threading import Timer

def showMatrix(m):
    fig = plt.figure()
    plt.imshow(m)
    plt.colorbar()
    plt.show()

def savePositionToFile(client, foldername="droneData", filename="position"):
    """Gets the position of the drone and saves it to the specified file in the specified folder"""
    
    pos = client.simGetVehiclePose().position
    try:
        with open(f'{foldername}/{filename}.txt', 'a') as f:
            f.write(f'{pos.x_val} {pos.y_val} {pos.z_val * -1}\n')
    except FileNotFoundError:
        print(f'Positional data not saved. Directory "{foldername}" not found.')

def loadPathFromPotreeJSON(foldername="paths", filename="potreePath"):
    """Returns a list of formatted points from a JSON file extracted from Potree"""
    import json
    import airsim

    with open(f'{foldername}/{filename}.json', 'r') as f:
        data = json.load(f)
        points = []
        for feature in data['features']:
            p = feature['geometry']['coordinates']

            # Invert the z-axis because AirSim uses NED coordinates
            points.append(airsim.Vector3r(p[0], p[1], p[2] * -1))

        return points[::-1]


def setImageFoldername(foldername="pics"):
    """ Increments the given foldername until it find a folder that is not taken """
    import os
    import airsim

    nameCounter = 0
    currentFoldername = foldername
    while os.path.exists(f'./pictures/{currentFoldername}'):
        currentFoldername = foldername + str(nameCounter)
        nameCounter += 1
    os.makedirs(f'./pictures/{currentFoldername}')
    return f'./pictures/{currentFoldername}'

