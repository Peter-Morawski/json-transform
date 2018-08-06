# -*- coding: utf-8 -*-

import unittest
from datastructure import ExtendedCar

EXTENDED_CAR_DICT = {
    ExtendedCar.FIELD_MODEL_NAME_NAME: "some car model",
    ExtendedCar.FIELD_MAX_SPEED_NAME: 130,
    ExtendedCar.FIELD_HORSEPOWER_NAME: 30
}


class DictDeserialization(unittest.TestCase):
    def test_extended_car(self):
        extended_car = ExtendedCar.from_json_dict(EXTENDED_CAR_DICT)

        self.assertIsNotNone(extended_car)
        assert extended_car.model_name == EXTENDED_CAR_DICT[ExtendedCar.FIELD_MODEL_NAME_NAME]
        assert extended_car.max_speed == EXTENDED_CAR_DICT[ExtendedCar.FIELD_MAX_SPEED_NAME]
        assert extended_car.horsepower == EXTENDED_CAR_DICT[ExtendedCar.FIELD_HORSEPOWER_NAME]

    def test_super_class_of_extended_car(self):
        self.skipTest("Needs to be implemented")

    def test_object_without_fields(self):
        self.skipTest("Needs to be implemented")

    def test_with_not_serializable_value(self):
        self.skipTest("Needs to be implemented")

    def test_with_json_object(self):
        self.skipTest("Needs to be implemented")

    def test_object_with_undefined_property(self):
        self.skipTest("Needs to be implemented")

    def test_object_with_missing_property(self):
        self.skipTest("Needs to be implemented")


class DictDeserializationTimestamps(unittest.TestCase):
    def test_date(self):
        self.skipTest("Needs to be implemented")

    def test_naive_datetime(self):
        self.skipTest("Needs to be implemented")

    def test_utc_datetime(self):
        self.skipTest("Needs to be implemented")

    def test_berlin_datetime(self):
        self.skipTest("Needs to be implemented")

    def test_istanbul_datetime(self):
        self.skipTest("Needs to be implemented")

    def test_tokyo_datetime(self):
        self.skipTest("Needs to be implemented")
