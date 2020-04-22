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

def loadPath(foldername="paths", filename="potreePath.json"):
    """Returns a list of formatted points from a JSON file extracted from Potree"""
    import json
    import airsim

    fSplit = filename.split(".")
    if len(fSplit) < 2:
        raise FileNotFoundError(f'{filename} not found. Remember to include filetype (e.g. .txt or .json)')



    filetype = fSplit[len(fSplit) - 1]

    if filetype == "txt":
        with open(f'{foldername}/{filename}', 'r') as f:
            points = []
            for line in f:
                p = line.strip().split(" ")
                points.append(airsim.Vector3r(float(p[0]), float(p[1]), float(p[2]) * -1))

            return points
    elif filetype == "json":
        with open(f'{foldername}/{filename}', 'r') as f:
            data = json.load(f)
            points = []
            for feature in data['features']:
                p = feature['geometry']['coordinates']

                # Invert the z-axis because AirSim uses NED coordinates
                points.append(airsim.Vector3r(p[0], p[1], p[2] * -1))

            return points
    else:
        raise NotImplementedError(f'Path filetype "{filetype}" is not supported.')


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