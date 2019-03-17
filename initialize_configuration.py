from argparse import ArgumentParser
from configuration.app_configuration import AppConfiguration, Bbox

if __name__ == "__main__":

    # Reading arguments
    parser = ArgumentParser()
    parser.add_argument("-c", "--coords", dest="coords", type=int, required=True, nargs='+')
    parser.add_argument("-b", "--background", dest="background", type=str, required=True,
                        default='resources/background.png')

    args = parser.parse_args()

    bbox = Bbox(args.coords[0], args.coords[1], args.coords[2], args.coords[3])
    conf = AppConfiguration(bbox, args.background)
    print('Configuration saved to config.xml')
