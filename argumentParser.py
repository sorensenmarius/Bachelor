import argparse
import errno
import string

pointDef = (100,0,-1)
pathDefFile = "defFile"
pathDefFolder = "defFolder"

def parseCLIargs():
    parser = argparse.ArgumentParser("Parses arguments from cli")

    parser.add_argument("-sl","-save_lidar",default=False ,action="store_true", help="Save lidar data to file.")
    
    parser.add_argument("-saveImage",default=False ,action="store_true", help="Save images during flight")
    parser.add_argument("-saveImageFolder",nargs=1, help= "Saves images to given folder.") 
    parser.add_argument("-savePos", default=False, action="store_true", help="Save drone position during flight to file.")
    parser.add_argument("-savePosFile", nargs=1, help= "Filename for drone positions.")

    parser.add_argument("-points", nargs=3,type= int,help="Specifies a goal point. Format: X Y Z")
    parser.add_argument("-path",nargs=1,help="Specifies a file to get a path of points from.")


    args = parser.parse_args() #Makes the namespace dict that will be returned

    if args.points == None and args.path == None:
        args.points = pointDef
        args.followPath = False
    elif args.points == None and args.path != None:
        args.path = args.path[0]
        args.followPath = True
    elif args.points != None:
        args.followPath = False  
    
    # Logic for the additional save features with specific file/folder names
    if args.saveImageFolder != None:
        args.saveImage = True
    if args.savePosFile != None:
        args.savePos = True

    return args