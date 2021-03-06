# -*- coding: utf-8 -*-

import datetime
import sys
import unittest

from jsontransform import ConfigurationError, ConstraintViolationError, MissingObjectError, _PY2, loadd
from .datastructure import Car, Container, ContainerWithFieldModeDecodeOnly, ContainerWithFieldModeEncodeOnly, \
    ExtendedCar, ExtendedExtendedCar, IssuePriority, JSONObjectWithRequiredField, JSONObjectWithoutFields


class DictDeserialization(unittest.TestCase):
    def test_automatic_target_object_recognition_with_unknown_json_object(self):
        with self.assertRaises(MissingObjectError):
            loadd({"some_unknown_field": "some value"})

    # noinspection PyMethodMayBeStatic
    def test_automatic_target_object_recognition_with_simple_object_1(self):
        actual = loadd({Container.CONTAINER_FIELD_NAME: "some value"})

        self.assertIsInstance(actual, Container)

    # noinspection PyMethodMayBeStatic
    def test_automatic_target_object_recognition_with_simple_object_2(self):
        actual = loadd({
            JSONObjectWithRequiredField.REQUIRED_FIELD_NAME: "value",
            JSONObjectWithRequiredField.SOME_FIELD_NAME: 42
        })

        self.assertIsInstance(actual, JSONObjectWithRequiredField)

    # noinspection PyMethodMayBeStatic
    def test_automatic_target_object_recognition_with_simple_object_3(self):
        actual = loadd({
            JSONObjectWithRequiredField.REQUIRED_FIELD_NAME: "value"
        })

        self.assertIsInstance(actual, JSONObjectWithRequiredField)

    def test_automatic_target_object_recognition_with_inheritance(self):
        d = {
            ExtendedCar.FIELD_MAX_SPEED_NAME: 265,
            ExtendedCar.FIELD_HORSEPOWER_NAME: 135,
            ExtendedCar.FIELD_MODEL_NAME_NAME: "extended car simple model"
        }
        actual = loadd(d)

        self.assertIsInstance(actual, ExtendedCar)

    def test_automatic_target_object_recognition_with_deeper_inheritance(self):
        d = {
            ExtendedExtendedCar.FIELD_MODEL_NAME_NAME: u"extended extended premium model",
            ExtendedExtendedCar.FIELD_HORSEPOWER_NAME: 1633,
            ExtendedExtendedCar.FIELD_MAX_SPEED_NAME: 400,
            ExtendedExtendedCar.FIELD_COLOR_NAME: u"white"
        }
        actual = loadd(d)

        self.assertIsInstance(actual, ExtendedExtendedCar)

    def test_automatic_target_object_recognition_with_two_objects_where_one_has_the_same_but_more_fields(self):
        d = {
            IssuePriority.NAME_NAME: u"critical",
            IssuePriority.ID_NAME: u"1",
            IssuePriority.ICON_URL_NAME: u"http://www.some-domain.com/some/path/icon.png"
        }
        actual = loadd(d)

        self.assertIsInstance(actual, IssuePriority)

    # noinspection PyMethodMayBeStatic
    def test_if_dict_is_casted_into_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some value"
        }
        actual = loadd(d, Container)
        self.assertIsInstance(actual, Container)

    def test_empty_dict_as_value(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {}
        }
        actual = loadd(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_none(self):
        d = {
            Container.CONTAINER_FIELD_NAME: None
        }
        actual = loadd(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_bool(self):
        d = {
            Container.CONTAINER_FIELD_NAME: True
        }
        actual = loadd(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_str(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some string"
        }
        actual = loadd(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_unicode(self):
        d = {
            Container.CONTAINER_FIELD_NAME: u"some unicode string"
        }
        actual = loadd(d, Container)

        if sys.version_info.major == _PY2:
            self.assertIsInstance(actual.container, unicode)

        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_int(self):
        d = {
            Container.CONTAINER_FIELD_NAME: 42
        }
        actual = loadd(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_float(self):
        d = {
            Container.CONTAINER_FIELD_NAME: 42.1337
        }
        actual = loadd(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    # noinspection PyMethodMayBeStatic
    def test_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                Container.CONTAINER_FIELD_NAME: "some string"
            }
        }
        actual = loadd(d, Container)
        self.assertIsInstance(actual.container, Container)

    def test_json_object_without_fields(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some string"
        }

        with self.assertRaises(ConfigurationError):
            loadd(d, JSONObjectWithoutFields)

    def test_wrong_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: "some string"
        }

        with self.assertRaises(TypeError):
            loadd(d, ExtendedCar)

    def test_not_deserializable_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: Container()
        }

        with self.assertRaises(TypeError):
            loadd(d, Container)

    def test_empty_list(self):
        d = {
            Container.CONTAINER_FIELD_NAME: []
        }
        actual = loadd(d, Container)
        self.assertEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_none(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [None, None, None]
        }
        actual = loadd(d, Container)
        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_bool(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [True, False, True]
        }
        actual = loadd(d, Container)
        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_empty_dict(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [{}]
        }
        actual = loadd(d, Container)
        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_str(self):
        d = {
            Container.CONTAINER_FIELD_NAME: ["some string", "another string", "aaaaaa strriiiiinggg"]
        }
        actual = loadd(d, Container)
        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_unicode(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [u"some unicode string", u"another unicode string", u"aaaaa"]
        }
        actual = loadd(d, Container)

        if sys.version_info.major == _PY2:
            for element in actual.container:
                self.assertIsInstance(element, unicode)

        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_int(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [1, 2, 3, 4, 5, 6]
        }
        actual = loadd(d, Container)
        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_float(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [1.123, 2.234, 3.345, 4.456]
        }
        actual = loadd(d, Container)
        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    # noinspection PyMethodMayBeStatic
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
        actual = loadd(d, Container)

        all(self.assertIsInstance(item, Container) for item in actual.container)

        expected = [loadd(item, Container) for item in d[Container.CONTAINER_FIELD_NAME]]
        for item in expected:
            self.assertTrue(any(item.container == actual_item.container for actual_item in actual.container))

    def test_list_with_not_deserializable_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [Container()]
        }

        with self.assertRaises(TypeError):
            loadd(d, Container)

    def test_list_with_list(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [[], [1, 2, 3], ["some string", "another string"]]
        }
        actual = loadd(d, Container)
        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_list_with_dict(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [{"key1": "some value", "key2": 1}, {"key1": 42}]
        }
        actual = loadd(d, Container)
        self.assertListEqual(d[Container.CONTAINER_FIELD_NAME], actual.container)

    def test_super_class_as_target_of_json_object(self):
        d = {
            ExtendedCar.FIELD_MODEL_NAME_NAME: "some car model",
            ExtendedCar.FIELD_MAX_SPEED_NAME: 130,
            ExtendedCar.FIELD_HORSEPOWER_NAME: 30
        }
        actual = loadd(d, Car)

        self.assertIsInstance(actual, Car)
        self.assertEqual(d[Car.FIELD_MODEL_NAME_NAME], actual.model_name)
        self.assertEqual(d[Car.FIELD_MAX_SPEED_NAME], actual.max_speed)

    # noinspection PyMethodMayBeStatic
    def test_dict_with_json_object(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                "key1": {
                    Container.CONTAINER_FIELD_NAME: "some string"
                }
            }
        }
        actual = loadd(d, Container)

        self.assertIsInstance(actual.container, dict)
        self.assertIsInstance(actual.container["key1"], Container)

    def test_date_from_unicode(self):
        d = {
            Container.CONTAINER_FIELD_NAME: u"2018-08-03"
        }
        actual = loadd(d)

        self.assertIsInstance(actual.container, datetime.date)
        self.assertNotIsInstance(actual.container, datetime.datetime)

    def test_datetime_from_unicode(self):
        d = {
            Container.CONTAINER_FIELD_NAME: u"2018-08-03T16:02:21Z"
        }
        actual = loadd(d)

        self.assertIsInstance(actual.container, datetime.datetime)

    def test_date_inside_list(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [u"2018-08-03"]
        }
        actual = loadd(d)

        self.assertIsInstance(actual.container[0], datetime.date)
        self.assertNotIsInstance(actual.container[0], datetime.datetime)

    def test_datetime_inside_list(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [u"2018-08-03T16:02:21Z"]
        }
        actual = loadd(d)

        self.assertIsInstance(actual.container[0], datetime.datetime)


class DictDeserializationWithRequiredField(unittest.TestCase):
    def test_missing_required_field(self):
        d = {
            JSONObjectWithRequiredField.SOME_FIELD_NAME: "some string"
        }

        with self.assertRaises(ConstraintViolationError):
            loadd(d, JSONObjectWithRequiredField)

    def test_satisfied_required_field(self):
        d = {
            JSONObjectWithRequiredField.SOME_FIELD_NAME: "some string",
            JSONObjectWithRequiredField.REQUIRED_FIELD_NAME: "another string"
        }
        actual = loadd(d, JSONObjectWithRequiredField)

        self.assertEqual(d[JSONObjectWithRequiredField.REQUIRED_FIELD_NAME], actual.required_field)

    def test_referenced_json_object_with_missing_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                JSONObjectWithRequiredField.SOME_FIELD_NAME: "some string",
            }
        }

        with self.assertRaises(ConstraintViolationError):
            loadd(d, Container)

    def test_list_with_json_object_with_missing_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [
                {
                    JSONObjectWithRequiredField.SOME_FIELD_NAME: "some string",
                }
            ]
        }

        with self.assertRaises(ConstraintViolationError):
            loadd(d, Container)

    def test_list_with_json_object_with_satisfied_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: [
                {
                    JSONObjectWithRequiredField.REQUIRED_FIELD_NAME: "some string"
                }
            ]
        }
        actual = loadd(d, Container)

        self.assertEqual(
            d[Container.CONTAINER_FIELD_NAME][0][JSONObjectWithRequiredField.REQUIRED_FIELD_NAME],
            actual.container[0].required_field
        )

    def test_dict_with_json_object_with_missing_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                "key1": {
                    JSONObjectWithRequiredField.SOME_FIELD_NAME: "some string"
                }
            }
        }

        with self.assertRaises(ConstraintViolationError):
            loadd(d, Container)

    def test_dict_with_json_object_with_satisfied_required_field(self):
        d = {
            Container.CONTAINER_FIELD_NAME: {
                "key1": {
                    JSONObjectWithRequiredField.REQUIRED_FIELD_NAME: "some string"
                }
            }
        }
        actual = loadd(d, Container)

        self.assertEqual(
            d[Container.CONTAINER_FIELD_NAME]["key1"][JSONObjectWithRequiredField.REQUIRED_FIELD_NAME],
            actual.container["key1"].required_field
        )


class DictDeserializationISO8601Compliance(unittest.TestCase):
    EXTENDED_DATE = "2018-08-13"
    BASIC_DATE = "20180813"
    EXTENDED_TIME = "16:31:12"
    BASIC_TIME = "163112"
    MICROSECOND = "265"
    EXTENDED_TIME_WITHOUT_SECOND = "16:31"
    BASIC_TIME_WITHOUT_SECOND = "1631"
    TIME_ONLY_HOUR = "16"
    EXTENDED_UTC_OFFSET = "+02:00"
    BASIC_UTC_OFFSET = "+0200"
    UTC_OFFSET_ONLY_HOUR = "+02"

    def setUp(self):
        self._d = {}

    def test_extended_date_format(self):
        self._d[Container.CONTAINER_FIELD_NAME] = self.EXTENDED_DATE
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.date)
        self.assertNotIsInstance(actual.container, datetime.datetime)
        self._assert_date(actual.container)

    def _assert_date(self, actual):
        self.assertEqual(actual.year, 2018)
        self.assertEqual(actual.month, 8)
        self.assertEqual(actual.day, 13)

    def test_basic_date_format(self):
        self._d[Container.CONTAINER_FIELD_NAME] = self.BASIC_DATE
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.date)
        self.assertNotIsInstance(actual.container, datetime.datetime)
        self._assert_date(actual.container)

    def test_extended_naive_datetime_with_extended_time(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}Z".format(self.EXTENDED_DATE, self.EXTENDED_TIME)
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime(actual.container)

    def _assert_naive_datetime(self, actual):
        self._assert_date(actual)
        self.assertEqual(actual.hour, 16)
        self.assertEqual(actual.minute, 31)
        self.assertEqual(actual.second, 12)

    def test_basic_naive_datetime_with_extended_time(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}Z".format(self.BASIC_DATE, self.EXTENDED_TIME)
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime(actual.container)

    def test_extended_naive_datetime_with_basic_time(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}Z".format(self.EXTENDED_DATE, self.BASIC_TIME)
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime(actual.container)

    def test_basic_naive_datetime_with_basic_time(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}Z".format(self.BASIC_DATE, self.BASIC_TIME)
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime(actual.container)

    def test_extended_naive_datetime_with_extended_time_with_microsecond(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}Z".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME,
            self.MICROSECOND
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime_with_microsecond(actual.container)

    def _assert_naive_datetime_with_microsecond(self, actual):
        self._assert_naive_datetime(actual)
        self.assertEqual(actual.microsecond, 265000)

    def test_basic_naive_datetime_with_extended_time_with_microsecond(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}Z".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME,
            self.MICROSECOND
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime_with_microsecond(actual.container)

    def test_extended_naive_datetime_with_basic_time_with_microsecond(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}Z".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME,
            self.MICROSECOND
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime_with_microsecond(actual.container)

    def test_basic_naive_datetime_with_basic_time_with_microsecond(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}Z".format(
            self.BASIC_DATE,
            self.BASIC_TIME,
            self.MICROSECOND
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime_with_microsecond(actual.container)

    def test_extended_naive_datetime_with_extended_time_without_second(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}Z".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME_WITHOUT_SECOND
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime_without_second(actual.container)

    def _assert_naive_datetime_without_second(self, actual):
        self._assert_date(actual)
        self.assertEqual(actual.hour, 16)
        self.assertEqual(actual.minute, 31)
        self.assertEqual(actual.second, 0)

    def test_basic_naive_datetime_with_extended_time_without_second(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}Z".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME_WITHOUT_SECOND
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime_without_second(actual.container)

    def test_extended_naive_datetime_with_basic_time_without_second(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}Z".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME_WITHOUT_SECOND
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime_without_second(actual.container)

    def test_basic_naive_datetime_with_basic_time_without_second(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}Z".format(
            self.BASIC_DATE,
            self.BASIC_TIME_WITHOUT_SECOND
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime_without_second(actual.container)

    def test_extended_naive_datetime_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}Z".format(self.EXTENDED_DATE, self.TIME_ONLY_HOUR)
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime_with_only_hour(actual.container)

    def _assert_naive_datetime_with_only_hour(self, actual):
        self._assert_date(actual)
        self.assertEqual(actual.hour, 16)
        self.assertEqual(actual.minute, 0)
        self.assertEqual(actual.second, 0)

    def test_basic_naive_datetime_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}Z".format(self.BASIC_DATE, self.TIME_ONLY_HOUR)
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_naive_datetime_with_only_hour(actual.container)

    def test_extended_date_with_extended_time_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def _assert_datetime_with_utc_offset(self, actual):
        self._assert_naive_datetime(actual)
        self._assert_utc_offset_is_right(actual)

    def _assert_utc_offset_is_right(self, actual):
        self.assertIsNotNone(actual.tzinfo)

        utc_offset = actual.tzinfo.utcoffset(actual)
        self.assertEqual(utc_offset.seconds, 2 * 60 * 60)

    def test_basic_date_with_extended_time_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_extended_date_with_extended_time_with_microsecond_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME,
            self.MICROSECOND,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def _assert_datetime_with_microsecond_and_utc_offset(self, actual):
        self._assert_naive_datetime_with_microsecond(actual)
        self._assert_utc_offset_is_right(actual)

    def test_basic_date_with_extended_time_with_microsecond_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME,
            self.MICROSECOND,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_extended_date_with_extended_time_without_second_and_with_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME_WITHOUT_SECOND,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def _assert_datetime_with_utc_offset_and_without_second(self, actual):
        self._assert_naive_datetime_without_second(actual)
        self._assert_utc_offset_is_right(actual)

    def test_basic_date_with_extended_time_without_second_and_with_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME_WITHOUT_SECOND,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def test_extended_date_with_time_with_only_hour_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.TIME_ONLY_HOUR,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_only_hour_and_utc_offset(actual.container)

    def _assert_datetime_with_only_hour_and_utc_offset(self, actual):
        self._assert_naive_datetime_with_only_hour(actual)
        self._assert_utc_offset_is_right(actual)

    def test_basic_date_with_time_with_only_hour_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.TIME_ONLY_HOUR,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_only_hour_and_utc_offset(actual.container)

    def test_extended_date_with_basic_time_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_basic_date_with_basic_time_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.BASIC_TIME,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_extended_date_with_basic_time_with_microsecond_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME,
            self.MICROSECOND,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_basic_date_with_basic_time_with_microsecond_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.BASIC_DATE,
            self.BASIC_TIME,
            self.MICROSECOND,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_extended_date_with_basic_time_without_second_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME_WITHOUT_SECOND,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def test_basic_date_with_basic_time_without_second_and_extended_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.BASIC_TIME_WITHOUT_SECOND,
            self.EXTENDED_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def test_extended_date_with_basic_time_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_basic_date_with_basic_time_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.BASIC_TIME,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_extended_date_with_basic_time_with_microsecond_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME,
            self.MICROSECOND,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_basic_date_with_basic_time_with_microsecond_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.BASIC_DATE,
            self.BASIC_TIME,
            self.MICROSECOND,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_extended_date_with_basic_time_without_second_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME_WITHOUT_SECOND,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def test_basic_date_with_basic_time_without_second_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.BASIC_TIME_WITHOUT_SECOND,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def test_extended_date_with_time_with_only_hour_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.TIME_ONLY_HOUR,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_only_hour_and_utc_offset(actual.container)

    def test_basic_date_with_time_with_only_hour_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.TIME_ONLY_HOUR,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_only_hour_and_utc_offset(actual.container)

    def test_extended_date_with_extended_time_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_basic_date_with_extended_time_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_extended_date_with_extended_time_with_microsecond_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME,
            self.MICROSECOND,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_basic_date_with_extended_time_with_microsecond_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME,
            self.MICROSECOND,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_extended_date_with_extended_time_without_second_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME_WITHOUT_SECOND,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def test_basic_date_with_extended_time_without_second_and_basic_utc_offset(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME_WITHOUT_SECOND,
            self.BASIC_UTC_OFFSET
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def test_extended_date_with_extended_time_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_basic_date_with_extended_time_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_extended_date_with_extended_time_with_microsecond_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME,
            self.MICROSECOND,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_basic_date_with_extended_time_with_microsecond_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME,
            self.MICROSECOND,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_extended_date_with_extended_time_without_second_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.EXTENDED_TIME_WITHOUT_SECOND,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def test_basic_date_with_extended_time_without_second_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.EXTENDED_TIME_WITHOUT_SECOND,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def test_extended_date_with_time_with_only_hour_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.TIME_ONLY_HOUR,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_only_hour_and_utc_offset(actual.container)

    def test_basic_date_with_time_with_only_hour_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.TIME_ONLY_HOUR,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_only_hour_and_utc_offset(actual.container)

    def test_extended_date_with_basic_time_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_basic_date_with_basic_time_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.BASIC_TIME,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset(actual.container)

    def test_extended_date_with_basic_time_with_microsecond_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME,
            self.MICROSECOND,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_basic_date_with_basic_time_with_microsecond_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}.{}{}".format(
            self.BASIC_DATE,
            self.BASIC_TIME,
            self.MICROSECOND,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_microsecond_and_utc_offset(actual.container)

    def test_extended_date_with_basic_time_without_second_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.EXTENDED_DATE,
            self.BASIC_TIME_WITHOUT_SECOND,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)

    def test_basic_date_with_basic_time_without_second_and_utc_offset_with_only_hour(self):
        self._d[Container.CONTAINER_FIELD_NAME] = "{}T{}{}".format(
            self.BASIC_DATE,
            self.BASIC_TIME_WITHOUT_SECOND,
            self.UTC_OFFSET_ONLY_HOUR
        )
        actual = loadd(self._d)

        self.assertIsInstance(actual.container, datetime.datetime)
        self._assert_datetime_with_utc_offset_and_without_second(actual.container)


class DictDeserializationWithFieldMode(unittest.TestCase):
    def setUp(self):
        self._d = {}

    def test_only_encodable_field(self):
        self._d[ContainerWithFieldModeEncodeOnly.ENCODE_ONLY_NAME] = "some_value"
        actual = loadd(self._d)

        self.assertIsInstance(actual, ContainerWithFieldModeEncodeOnly)
        self.assertNotEqual(self._d[ContainerWithFieldModeEncodeOnly.ENCODE_ONLY_NAME], actual.encode_only)

    def test_only_decodable_field(self):
        self._d[ContainerWithFieldModeDecodeOnly.DECODE_ONLY_NAME] = "some_value"
        actual = loadd(self._d)

        self.assertIsInstance(actual, ContainerWithFieldModeDecodeOnly)
        self.assertEqual(self._d[ContainerWithFieldModeDecodeOnly.DECODE_ONLY_NAME], actual.decode_only)
