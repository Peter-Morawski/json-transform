# -*- coding: utf-8 -*-

import unittest
import datetime
from jsontransform import ConfigurationError, FieldValidationError, MissingObjectError, Deserializer
from .datastructure import ExtendedCar, Car, Container, JsonObjectWithoutFields, JsonObjectWithRequiredField, \
    JsonObjectWithNotNullableField
from .common import get_new_york_utc_offset, get_new_york_utc_offset_as_int


class DictDeserialization(unittest.TestCase):
    def test_not_found_json_object(self):
        with self.assertRaises(MissingObjectError):
            Deserializer.from_json_dict({"some_unknown_field": "some value"})

    def test_automatic_target_object_recognition_1(self):
        actual = Deserializer.from_json_dict({Container.CONTAINER_FIELD_NAME: "some value"})

        assert type(actual) is Container

    def test_automatic_target_object_recognition_2(self):
        actual = Deserializer.from_json_dict({
            JsonObjectWithRequiredField.REQUIRED_FIELD_NAME: "value",
            JsonObjectWithRequiredField.SOME_FIELD_NAME: 42
        })

        assert type(actual) is JsonObjectWithRequiredField

    def test_automatic_target_object_recognition_3(self):
        actual = Deserializer.from_json_dict({
            JsonObjectWithRequiredField.REQUIRED_FIELD_NAME: "value"
        })

        assert type(actual) is JsonObjectWithRequiredField

    def test_if_dict_is_casted_into_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some value"
        }
        actual = Deserializer.from_json_dict(d, Container)
        assert type(actual) is Container

    def test_empty_dict_as_value(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {}
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_none(self):
        d = {
            Container.CONTAINER_FIELD_NAME: None
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_str(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some string"
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_int(self):
        d = {
            Container.CONTAINER_FIELD_NAME: 42
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_float(self):
        d = {
            Container.CONTAINER_FIELD_NAME: 42.1337
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                Container.CONTAINER_FIELD_NAME: "some string"
            }
        }
        actual = Deserializer.from_json_dict(d, Container)
        assert type(actual.container) is Container

    def test_json_object_without_fields(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some string"
        }

        with self.assertRaises(ConfigurationError):
            Deserializer.from_json_dict(d, JsonObjectWithoutFields)

    def test_wrong_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some string"
        }

        with self.assertRaises(TypeError):
            Deserializer.from_json_dict(d, ExtendedCar)

    def test_not_deserializable_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: Container()
        }

        with self.assertRaises(TypeError):
            Deserializer.from_json_dict(d, Container)

    def test_empty_list(self):
        d = {
            Container.CONTAINER_FIELD_NAME: []
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_none(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [None, None, None]
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_empty_dict(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [{}]
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_str(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["some string", "another string", "aaaaaa strriiiiinggg"]
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_int(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [1, 2, 3, 4, 5, 6]
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_float(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [1.123, 2.234, 3.345, 4.456]
        }
        actual = Deserializer.from_json_dict(d, Container)
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
        actual = Deserializer.from_json_dict(d, Container)

        assert all(type(item) is Container for item in actual.container)

        expected = [Deserializer.from_json_dict(item, Container) for item in d[Container.CONTAINER_FIELD_NAME]]
        for item in expected:
            assert any(item.container == actual_item.container for actual_item in actual.container)

    def test_list_with_not_deserializable_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [Container()]
        }

        with self.assertRaises(TypeError):
            Deserializer.from_json_dict(d, Container)

    def test_list_with_list(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [[], [1, 2, 3], ["some string", "another string"]]
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_dict(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [{"key1": "some value", "key2": 1}, {"key1": 42}]
        }
        actual = Deserializer.from_json_dict(d, Container)
        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_super_class_of_json_object(self):
        d = {
            ExtendedCar.FIELD_MODEL_NAME_NAME: "some car model",
            ExtendedCar.FIELD_MAX_SPEED_NAME: 130,
            ExtendedCar.FIELD_HORSEPOWER_NAME: 30
        }
        actual = Deserializer.from_json_dict(d, Car)

        assert type(actual) is Car
        self.assertEqual(d[Car.FIELD_MODEL_NAME_NAME], actual.model_name)
        self.assertEqual(d[Car.FIELD_MAX_SPEED_NAME], actual.max_speed)

    def test_dict_with_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                "key1": {
                    Container.CONTAINER_FIELD_NAME: "some string"
                }
            }
        }
        actual = Deserializer.from_json_dict(d, Container)

        assert type(actual.container) is dict
        assert type(actual.container["key1"]) is Container


class DictDeserializationTimes(unittest.TestCase):
    DATE = "2018-08-13"
    TIME = "16:00:00"

    def test_date(self):
        d = {
            Container.CONTAINER_FIELD_NAME: self.DATE
        }
        actual = Deserializer.from_json_dict(d, Container)

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
        actual = Deserializer.from_json_dict(d, Container)

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
        actual = Deserializer.from_json_dict(d, Container)

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
        actual = Deserializer.from_json_dict(d, Container)

        assert type(actual.container) is str

    def test_naive_datetime_with_missing_time_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "{}T{}".format(self.DATE, self.TIME)
        }
        actual = Deserializer.from_json_dict(d, Container)

        assert type(actual.container) is str

    def test_datetime_with_timezone_with_missing_timezone_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "{}T{}0000".format(self.DATE, self.TIME)
        }
        actual = Deserializer.from_json_dict(d, Container)

        assert type(actual.container) is str

    def test_list_with_date(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [self.DATE]
        }
        actual = Deserializer.from_json_dict(d, Container)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is datetime.date
        assert type(actual.container[0]) is not datetime.datetime
        self._assert_date_equal(actual.container[0])

    def test_list_with_naive_datetime(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["{}T{}Z".format(self.DATE, self.TIME)]
        }
        actual = Deserializer.from_json_dict(d, Container)

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
        actual = Deserializer.from_json_dict(d, Container)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is datetime.datetime
        self._assert_datetime_equal(actual.container[0])
        self.assertIsNotNone(actual.container[0].tzinfo)

        self._check_datetime_utc_offset(actual.container[0], utc_offset_hours)

    def test_list_with_broken_naive_datetime_with_missing_date_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["{}{}Z".format(self.DATE, self.TIME)]
        }
        actual = Deserializer.from_json_dict(d, Container)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is str

    def test_list_with_broken_naive_datetime_with_missing_time_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["{}T{}".format(self.DATE, self.TIME)]
        }
        actual = Deserializer.from_json_dict(d, Container)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is str

    def test_list_with_broken_datetime_with_timezone_with_missing_timezone_character(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["{}T{}{}".format(self.DATE, self.TIME, "0000")]
        }
        actual = Deserializer.from_json_dict(d, Container)

        assert len(actual.container) == 1
        assert type(actual.container[0]) is str


class DictDeserializationWithRequiredField(unittest.TestCase):
    def test_missing_required_field(self):
        d = {
            JsonObjectWithRequiredField.SOME_FIELD_NAME: "some string"
        }

        with self.assertRaises(FieldValidationError):
            Deserializer.from_json_dict(d, JsonObjectWithRequiredField)

    def test_satisfied_required_field(self):
        d = {
            JsonObjectWithRequiredField.SOME_FIELD_NAME: "some string",
            JsonObjectWithRequiredField.REQUIRED_FIELD_NAME: "another string"
        }
        actual = Deserializer.from_json_dict(d, JsonObjectWithRequiredField)

        self.assertEqual(d[JsonObjectWithRequiredField.REQUIRED_FIELD_NAME], actual.required_field)

    def test_referenced_json_object_with_missing_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                JsonObjectWithRequiredField.SOME_FIELD_NAME: "some string",
            }
        }

        with self.assertRaises(FieldValidationError):
            Deserializer.from_json_dict(d, Container)

    def test_list_with_json_object_with_missing_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [
                {
                    JsonObjectWithRequiredField.SOME_FIELD_NAME: "some string",
                }
            ]
        }

        with self.assertRaises(FieldValidationError):
            Deserializer.from_json_dict(d, Container)

    def test_list_with_json_object_with_satisfied_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [
                {
                    JsonObjectWithRequiredField.REQUIRED_FIELD_NAME: "some string"
                }
            ]
        }
        actual = Deserializer.from_json_dict(d, Container)

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
            Deserializer.from_json_dict(d, Container)

    def test_dict_with_json_object_with_satisfied_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                "key1": {
                    JsonObjectWithRequiredField.REQUIRED_FIELD_NAME: "some string"
                }
            }
        }
        actual = Deserializer.from_json_dict(d, Container)

        self.assertEqual(
            d[Container.CONTAINER_FIELD_NAME]["key1"][JsonObjectWithRequiredField.REQUIRED_FIELD_NAME],
            actual.container["key1"].required_field
        )


class DictDeserializationWithNotNullable(unittest.TestCase):
    def test_not_nullable_field_which_is_null(self):
        d = {
            JsonObjectWithNotNullableField.NOT_NULLABLE_NAME: None
        }

        with self.assertRaises(FieldValidationError):
            Deserializer.from_json_dict(d, JsonObjectWithNotNullableField)

    def test_referenced_json_object_with_not_nullable_field_which_is_null(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                JsonObjectWithNotNullableField.NOT_NULLABLE_NAME: None
            }
        }

        with self.assertRaises(FieldValidationError):
            Deserializer.from_json_dict(d, Container)

    def test_list_with_json_object_with_not_nullable_field_which_is_null(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [
                {
                    JsonObjectWithNotNullableField.NOT_NULLABLE_NAME: None
                }
            ]
        }

        with self.assertRaises(FieldValidationError):
            Deserializer.from_json_dict(d, Container)

    def test_dict_with_json_object_with_not_nullable_field_which_is_null(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                "key1": {
                    JsonObjectWithNotNullableField.NOT_NULLABLE_NAME: None
                }
            }
        }

        with self.assertRaises(FieldValidationError):
            Deserializer.from_json_dict(d, Container)
