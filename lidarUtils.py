import setup_path
import airsim

import numpy
import time

def parseLidarData(data):
    """Reshapes the lidarData object to an array of [X,Y,Z]"""
    if len(data.point_cloud) > 2:
        points = numpy.array(data.point_cloud, dtype=numpy.dtype('f4'))
        points = numpy.reshape(points, (int(points.shape[0]/3), 3))
        return points
    return None

def writeLidarDataToDisk(data, foldername, filename):
    """Writes the lidar data to the spicified folder with the specified file name"""
    try:
        with open(f'{foldername}/{filename}.txt', 'a') as f:
            for point in data:
                f.write(f'{point[0]} {point[1]} {point[2] * -1}\n')
    except FileNotFoundError:
        print(f'LidarData not saved. File "./{foldername}/{filename}" not found.')


def getLidarData(client):
    """Gets and returns the formatted list of lidar data"""
    d = client.getLidarData(lidar_name="Lidar")
    if len(d.point_cloud) < 3:
        print("No points received in lidar data")
        return []
    else:
        return parseLidarData(d)

def handleLidarData(client, foldername = "lidarData", filename = "point_cloud"):
    """Gets lidar data and saves it to a file"""
    p = getLidarData(client)
    writeLidarDataToDisk(p, foldername, filename)
        