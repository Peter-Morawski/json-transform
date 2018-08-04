# -*- coding: utf-8 -*-

import unittest
from serialization import DictSerialization


def create_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DictSerialization))
    # suite.addTest(unittest.makeSuite(DictSerializationWithDates))

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(create_test_suite())
