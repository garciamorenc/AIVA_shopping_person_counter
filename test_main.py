import unittest


def run(path):
    loader = unittest.TestLoader()
    start_dir = path
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":

    path = './unit_test'
    run(path)
