import unittest
from argparse import ArgumentParser


def run(path):
    loader = unittest.TestLoader()
    start_dir = path
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":

    # Reading arguments
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", type=str, default='./unit_test')

    args = parser.parse_args()

    run(args.path)
