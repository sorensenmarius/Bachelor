import argparse

def parseCLIargs():
    try:
        parser = argparse.ArgumentParser("Parses arguments from cli")
        parser.add_argument("-sl","-save_lidar",default=False ,action="store_true")
        parser.add_argument("-saveImage",default=False ,action="store_true")
        parser.add_argument("-savePos")

        parser.add_argument("-points", nargs=3,help="Specifies a point the \
        drone will try to reach")
        parser.add_argument("-path",nargs=1, help="Specifies a path the \
        drone will try to reach from a given file")

        args = parser.parse_args()
        if args.points == None and args.path == None:
            return SyntaxError
        print(args)
        return args
    except:
        pass

if __name__ == "__main__":
    inputten = parseCLIargs()