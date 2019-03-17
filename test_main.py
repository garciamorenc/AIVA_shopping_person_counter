import unittest


def run(test_path):
    loader = unittest.TestLoader()
    start_dir = test_path
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":

    path = './unit_test'
    run(path)
