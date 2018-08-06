# -*- coding: utf-8 -*-

import unittest
from tests.serialization import DictSerialization, DictSerializationWithTimes
from tests.deserialization import DictDeserialization


def create_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DictSerialization))
    suite.addTest(unittest.makeSuite(DictSerializationWithTimes))
    suite.addTests(unittest.makeSuite(DictDeserialization))

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, failfast=False)
    result = runner.run(create_test_suite())

    if result.failures or result.errors:
        exit(1)
