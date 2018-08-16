# -*- coding: utf-8 -*-

import unittest
import datetime
from jsontransform import ConfigurationError, FieldValidationError
from .datastructure import ExtendedCar, Car, Container, JsonObjectWithoutFields, JsonObjectWithRequiredField
from .common import get_new_york_utc_offset, get_new_york_utc_offset_as_int


class DictDeserialization(unittest.TestCase):
    def test_if_dict_is_casted_into_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some value"
        }
        actual = Container.from_json_dict(d)
        assert type(actual) is Container

    def test_empty_dict(self):
        with self.assertRaises(TypeError):
            Container.from_json_dict({})

    def test_none_instead_of_dict(self):
        with self.assertRaises(TypeError):
            Container.from_json_dict(None)

    def test_empty_dict_as_value(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {}
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_none(self):
        d = {
            Container.CONTAINER_FIELD_NAME: None
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_str(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some string"
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_int(self):
        d = {
            Container.CONTAINER_FIELD_NAME: 42
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_float(self):
        d = {
            Container.CONTAINER_FIELD_NAME: 42.1337
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                Container.CONTAINER_FIELD_NAME: "some string"
            }
        }
        actual = Container.from_json_dict(d)
        assert type(actual.container) is Container

    def test_json_object_without_fields(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some string"
        }

        with self.assertRaises(ConfigurationError):
            JsonObjectWithoutFields.from_json_dict(d)

    def test_wrong_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some string"
        }

        with self.assertRaises(TypeError):
            ExtendedCar.from_json_dict(d)

    def test_not_deserializable_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: Container()
        }

        with self.assertRaises(TypeError):
            Container.from_json_dict(d)

    def test_empty_list(self):
        d = {
            Container.CONTAINER_FIELD_NAME: []
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_none(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [None, None, None]
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_empty_dict(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [{}]
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_str(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["some string", "another string", "aaaaaa strriiiiinggg"]
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_int(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [1, 2, 3, 4, 5, 6]
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_float(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [1.123, 2.234, 3.345, 4.456]
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [
                {
                    Container.CONTAINER_FIELD_NAME: "some string"
                },
                {
                    Container.CONTAINER_FIELD_NAME: 1
                }
            ]
        }
        actual = Container.from_json_dict(d)

        assert all(type(item) is Container for item in actual.container)

        expected = [Container.from_json_dict(item) for item in d[Container.CONTAINER_FIELD_NAME]]
        for item in expected:
            assert any(item.container == actual_item.container for actual_item in actual.container)

    def test_list_with_not_deserializable_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [Container()]
        }

        with self.assertRaises(TypeError):
            Container.from_json_dict(d)

    def test_list_with_list(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [[], [1, 2, 3], ["some string", "another string"]]
        }
        actual = Container.from_json_dict(d)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_dict(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [{"key1": "some value", "key2": 1}, {"key1": 42}]
        }
        actual = Container.from_json_dict(d)
        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_super_class_of_json_object(self):
        d = {
            ExtendedCar.FIELD_MODEL_NAME_NAME: "some car model",
            ExtendedCar.FIELD_MAX_SPEED_NAME: 130,
            ExtendedCar.FIELD_HORSEPOWER_NAME: 30
        }
        actual = Car.from_json_dict(d)

        assert type(actual) is Car
        self.assertEqual(d[Car.FIELD_MODEL_NAME_NAME], actual.model_name)
        self.assertEqual(d[Car.FIELD_MAX_SPEED_NAME], actual.max_speed)


class DictDeserializationTimes(unittest.TestCase):
    DATE = "2018-08-13"
    TIME = "16:00:00"

    def test_date(self):
        d = {
            Container.CONTAINER_FIELD_NAME: self.DATE
        }
        actual = Container.from_json_dict(d)

        assert type(actual) is Container
        assert type(actual.container) is datetime.date
        assert type(actual.container) is not datetime.datetime

        self._assert_date_equal(actual.container)

    def _assert_date_equal(self, d):
        self.assertEqual(2018, d.year)
        self.assertEqual(8, d.month)
        self.assertEqual(13, d.day)

    def test_naive_datetime(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "{}T{}Z".format(self.DATE, self.TIME)
        }
        actual = Container.from_json_dict(d)

        assert type(actual) is Container
        assert type(actual.container) is datetime.datetime

        self._assert_datetime_equal(actual.container)

    def _assert_datetime_equal(self, d):
        self._assert_date_equal(d)
        self.assertEqual(16, d.hour)
        self.assertEqual(0, d.minute)
        self.assertEqual(0, d.second)

    def test_utc_datetime(self):
        self._datetime_timezone_helper("+0000", 0)

    def test_berlin_datetime(self):
        self._datetime_timezone_helper("+0200", 2)

    def test_london_datetime(self):
        self._datetime_timezone_helper("+0100", 1)

    def test_istanbul_datetime(self):
        self._datetime_timezone_helper("+0300", 3)

    def test_tokyo_datetime(self):
        self._datetime_timezone_helper("+0900", 9)

    def test_new_york_datetime(self):
        self._datetime_timezone_helper(get_new_york_utc_offset(), get_new_york_utc_offset_as_int())

    def _datetime_timezone_helper(self, utc_offset, utc_offset_hours):
        d = {
            Container.CONTAINER_FIELD_NAME: "{}T{}{}".format(self.DATE, self.TIME, utc_offset)
        }
        actual = Container.from_json_dict(d)

        assert type(actual.container) is datetime.datetime
        self._assert_datetime_equal(actual.container)
        self.assertIsNotNone(actual.container.tzinfo)

        self._check_datetime_utc_offset(actual.container, utc_offset_hours)

    def _check_datetime_utc_offset(self, dt, expected_offset_hours):
        utc_offset = dt.tzinfo.utcoffset(dt)

        if utc_offset.days == -1:
            actual_offset = utc_offset.seconds if utc_offset.seconds == 0 else ((utc_offset.seconds / 60) / 60) - 24
        else:
            actual_offset = utc_offset.seconds if utc_offset.seconds == 0 else (utc_offset.seconds / 60) / 60
        assert actual_offset == expected_offset_hours

    def test_naive_datetime_with_missing_date_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "{}{}Z".format(self.DATE, self.TIME)
        }
        actual = Container.from_json_dict(d)

        assert type(actual.container) is str

    def test_naive_datetime_with_missing_time_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "{}T{}".format(self.DATE, self.TIME)
        }
        actual = Container.from_json_dict(d)

        assert type(actual.container) is str

    def test_datetime_with_timezone_with_missing_timezone_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "{}T{}0000".format(self.DATE, self.TIME)
        }
        actual = Container.from_json_dict(d)

        assert type(actual.container) is str

    def test_list_with_date(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [self.DATE]
        }
        actual = Container.from_json_dict(d)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is datetime.date
        assert type(actual.container[0]) is not datetime.datetime
        self._assert_date_equal(actual.container[0])

    def test_list_with_naive_datetime(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["{}T{}Z".format(self.DATE, self.TIME)]
        }
        actual = Container.from_json_dict(d)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is datetime.datetime
        self._assert_datetime_equal(actual.container[0])

    def test_list_with_utc_datetime(self):
        self._list_with_datetime_with_timezone_helper("+0000", 0)

    def test_list_with_berlin_datetime(self):
        self._list_with_datetime_with_timezone_helper("+0200", 2)

    def test_list_with_london_datetime(self):
        self._list_with_datetime_with_timezone_helper("+0100", 1)

    def test_list_with_istanbul_datetime(self):
        self._list_with_datetime_with_timezone_helper("+0300", 3)

    def test_list_with_tokyo_datetime(self):
        self._list_with_datetime_with_timezone_helper("+0900", 9)

    def test_list_with_new_york_datetime(self):
        self._list_with_datetime_with_timezone_helper(get_new_york_utc_offset(), get_new_york_utc_offset_as_int())

    def _list_with_datetime_with_timezone_helper(self, utc_offset, utc_offset_hours):
        d = {
            Container.CONTAINER_FIELD_NAME: ["{}T{}{}".format(self.DATE, self.TIME, utc_offset)]
        }
        actual = Container.from_json_dict(d)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is datetime.datetime
        self._assert_datetime_equal(actual.container[0])
        self.assertIsNotNone(actual.container[0].tzinfo)

        self._check_datetime_utc_offset(actual.container[0], utc_offset_hours)

    def test_list_with_broken_naive_datetime_with_missing_date_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["{}{}Z".format(self.DATE, self.TIME)]
        }
        actual = Container.from_json_dict(d)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is str

    def test_list_with_broken_naive_datetime_with_missing_time_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["{}T{}".format(self.DATE, self.TIME)]
        }
        actual = Container.from_json_dict(d)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is str

    def test_list_with_broken_datetime_with_timezone_with_missing_timezone_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["{}T{}{}".format(self.DATE, self.TIME, "0000")]
        }
        actual = Container.from_json_dict(d)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is str


class DictDeserializationWithRequiredField(unittest.TestCase):
    def setUp(self):
        self._container = JsonObjectWithRequiredField()

    def test_missing_required_field(self):
        d = {
            JsonObjectWithRequiredField.SOME_FIELD_NAME: "some string"
        }

        with self.assertRaises(FieldValidationError):
            JsonObjectWithRequiredField.from_json_dict(d)

    def test_satisfied_required_field(self):
        d = {
            JsonObjectWithRequiredField.SOME_FIELD_NAME: "some string",
            JsonObjectWithRequiredField.REQUIRED_FIELD_NAME: "another string"
        }
        actual = JsonObjectWithRequiredField.from_json_dict(d)

        self.assertEqual(d[JsonObjectWithRequiredField.REQUIRED_FIELD_NAME], actual.required_field)

    def test_referenced_json_object_with_missing_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                JsonObjectWithRequiredField.SOME_FIELD_NAME: "some string",
            }
        }

        with self.assertRaises(FieldValidationError):
            Container.from_json_dict(d)

    def test_list_with_json_object_with_missing_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [
                {
                    JsonObjectWithRequiredField.SOME_FIELD_NAME: "some string",
                }
            ]
        }

        with self.assertRaises(FieldValidationError):
            Container.from_json_dict(d)

    def test_list_with_json_object_with_satisfied_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [
                {
                    JsonObjectWithRequiredField.REQUIRED_FIELD_NAME: "some string"
                }
            ]
        }
        actual = Container.from_json_dict(d)

        self.assertEqual(
            d[Container.CONTAINER_FIELD_NAME][0][JsonObjectWithRequiredField.REQUIRED_FIELD_NAME],
            actual.container[0].required_field
        )

    def test_dict_with_json_object_with_missing_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                "key1": {
                    JsonObjectWithRequiredField.SOME_FIELD_NAME: "some string"
                }
            }
        }

        with self.assertRaises(FieldValidationError):
            Container.from_json_dict(d)

    def test_dict_with_json_object_with_satisfied_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                "key1": {
                    JsonObjectWithRequiredField.REQUIRED_FIELD_NAME: "some string"
                }
            }
        }
        actual = Container.from_json_dict(d)

        self.assertEqual(
            d[Container.CONTAINER_FIELD_NAME]["key1"][JsonObjectWithRequiredField.REQUIRED_FIELD_NAME],
            actual.container["key1"].required_field
        )
