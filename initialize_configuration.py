from argparse import ArgumentParser
from configuration.app_configuration import AppConfiguration, Bbox

if __name__ == "__main__":

    # Reading arguments
    parser = ArgumentParser()
    parser.add_argument("-c", "--coords", dest="coords", type=int, required=True, nargs='+')

    args = parser.parse_args()

    bbox = Bbox(args.coords[0], args.coords[1], args.coords[2], args.coords[3])
    conf = AppConfiguration(bbox)
    # TODO meter background en configuracion
    print('Configuration saved to config.xml')
