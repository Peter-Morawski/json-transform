# -*- coding: utf-8 -*-

import unittest

from tests.deserialization import DictDeserialization, DictDeserializationISO8601Compliance, \
    DictDeserializationWithFieldMode, DictDeserializationWithRequiredField
from tests.serialization import DictSerialization, DictSerializationWithFieldMode, DictSerializationWithTimes


def create_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DictSerialization))
    suite.addTest(unittest.makeSuite(DictSerializationWithTimes))
    suite.addTests(unittest.makeSuite(DictDeserialization))
    suite.addTest(unittest.makeSuite(DictDeserializationWithRequiredField))
    suite.addTest(unittest.makeSuite(DictDeserializationISO8601Compliance))
    suite.addTests(unittest.makeSuite(DictDeserializationWithFieldMode))
    suite.addTests(unittest.makeSuite(DictSerializationWithFieldMode))

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2, failfast=False)
    result = runner.run(create_test_suite())

    if result.failures or result.errors:
        exit(1)
