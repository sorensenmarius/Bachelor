import matplotlib.pyplot as plt

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