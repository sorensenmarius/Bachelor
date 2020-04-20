import argparse
import errno
import string

pointDef = (100,0,-1)
pathDefFile = "defFile"
pathDefFolder = "defFolder"

def parseCLIargs():
    parser = argparse.ArgumentParser("Parses arguments from cli")

    parser.add_argument("-sl","-save_lidar",default=False ,action="store_true")
    
    parser.add_argument("-saveImage",default=False ,action="store_true")
    parser.add_argument("-saveImageFolder",nargs=1) #With foldername location
    parser.add_argument("-savePos", default=False, action="store_true")
    parser.add_argument("-savePosFile", nargs=1) #With filename location

    parser.add_argument("-points", nargs=3,type= int,help="Specifies a point the \
    drone will try to reach. Format: -points x y z")
    parser.add_argument("-path",nargs=1,help="Specifies a path the \
    drone will try to reach from a given file. Format: -path filename")

    args = parser.parse_args() #Makes the namespace dict that will be returned
    
    if args.points == None and args.path == None:
        args.points = pointDef
        args.followPath = False
    elif args.points == None and args.path != None:
        print(args.path[0])
        args.path = checkF(args.path[0])
        args.followPath = True
    elif args.points != None:
        args.followPath = False  
    
    # Logic for the additional save features with specific file/folder names
    if args.saveImageFolder != None:
        args.saveImage = True
    if args.savePosFile != None:
        args.savePos = True

    #More args?
    return args

def checkF(fileName):
    try:
        with open(fileName) as f:
            x = f.read()
            return fileName
    except IOError as e:
        if e.errno == errno.ENOENT:
            print("File/Folder "+fileName+" does not exist")
            return pathDefFile
        elif f.errno == errno.EACCES:
            print("File/Folder "+fileName+" cannot be read")
            return pathDefFile
        else:
            print("Other error with "+fileName)
            return pathDefFile


if __name__ == "__main__":
    inputten = parseCLIargs()
