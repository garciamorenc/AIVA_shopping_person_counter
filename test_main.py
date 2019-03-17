import unittest


def run(test_path):
    """
    Run all the test of the path
    :param test_path: path with test files
    """
    loader = unittest.TestLoader()
    start_dir = test_path
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":

    path = './unit_test'
    run(path)
