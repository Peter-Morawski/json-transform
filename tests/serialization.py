# -*- coding: utf-8 -*-

import unittest
import datetime
from .datastructure import JsonObjectWithoutFields, NotSerializableObject, ExtendedCar, Container, \
    ContainerWithSomeDecoratorBeforeField, ContainerWithSomeDecoratorAfterField, JsonObjectWithNotNullableField
from jsontransform import ConfigurationError, DATE_FORMAT, DATETIME_FORMAT, DATETIME_TZ_FORMAT, FieldValidationError, \
    Serializer
from dateutil import tz
from .common import get_new_york_utc_offset


class DictSerialization(unittest.TestCase):
    def setUp(self):
        self._container = Container()

    def test_json_object_with_some_decorator_before_field_decorator(self):
        self._container = ContainerWithSomeDecoratorBeforeField()
        self._container.container = "some string"
        actual = Serializer.to_json_dict(self._container)

        self.assertIn(Container.CONTAINER_FIELD_NAME, actual.keys())

    def test_json_object_with_some_decorator_after_field_decorator(self):
        self._container = ContainerWithSomeDecoratorAfterField()
        self._container.container = "some value"
        actual = Serializer.to_json_dict(self._container)

        self.assertIn(Container.CONTAINER_FIELD_NAME, actual.keys())

    def test_none(self):
        self._container.container = None
        actual = Serializer.to_json_dict(self._container)

        self.assertEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_str(self):
        self._container.container = "some string"
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is str
        self.assertEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_int(self):
        self._container.container = 42
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is int
        self.assertEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_float(self):
        self._container.container = 42.1337
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is float
        self.assertEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_json_object(self):
        self._container.container = Container()
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict
        self.assertDictEqual(Serializer.to_json_dict(self._container.container), actual[Container.CONTAINER_FIELD_NAME])

    def test_json_object_without_fields(self):
        self._container.container = JsonObjectWithoutFields()

        with self.assertRaises(ConfigurationError):
            Serializer.to_json_dict(self._container)

    def test_not_serializable_object(self):
        self._container.container = NotSerializableObject()

        with self.assertRaises(TypeError):
            Serializer.to_json_dict(self._container)

    def test_empty_list(self):
        self._container.container = []
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list
        self.assertListEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_none(self):
        self._container.container = [None, None, None]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list
        self.assertListEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_str(self):
        self._container.container = ["some string", "another string"]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list
        self.assertListEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_int(self):
        self._container.container = [1, 2, 3, 4]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list
        self.assertListEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_float(self):
        self._container.container = [1.123, 2.123, 3.123, 4.123]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list
        self.assertListEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_json_object(self):
        self._container.container = [Container(), Container(), Container()]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [Serializer.to_json_dict(item) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_json_object_without_fields(self):
        self._container.container = [JsonObjectWithoutFields(), JsonObjectWithoutFields()]

        with self.assertRaises(ConfigurationError):
            Serializer.to_json_dict(self._container)

    def test_list_with_not_serializable_object(self):
        self._container.container = [NotSerializableObject(), NotSerializableObject()]

        with self.assertRaises(TypeError):
            Serializer.to_json_dict(self._container)

    def test_list_with_list(self):
        self._container.container = [
            [],
            [1, 2, 3],
            [1.111, 2.12356],
            ["some string"],
            [None, None, None],
            [Container(), Container()],
        ]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [item for item in self._container.container]
        for lst in expected:
            for i, item in enumerate(lst):
                if type(item) is Container:
                    lst[i] = Serializer.to_json_dict(lst[i])

        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_tuple(self):
        self._container.container = [tuple([]), tuple([1, 2, 3])]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [list(item) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_set(self):
        self._container.container = [set([]), {1, 2, 3}]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [list(item) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_dict(self):
        self._container.container = [{"key1": "", "key2": None}, {"key1": 1, "key2": 1.123}]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list
        for index, item in enumerate(actual[Container.CONTAINER_FIELD_NAME]):
            self.assertDictEqual(item, self._container.container[index])

    def test_empty_tuple(self):
        self._container.container = tuple([])
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_none(self):
        self._container.container = (None, None, None)
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_str(self):
        self._container.container = ("some string", "another string", "and another string...")
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_int(self):
        self._container.container = (1, 2, 3, 4)
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_float(self):
        self._container.container = (1.123, 2.123, 3.1337)
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_json_object(self):
        self._container.container = (Container(), Container(), Container())
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [Serializer.to_json_dict(item) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_json_object_without_fields(self):
        self._container.container = (JsonObjectWithoutFields(), JsonObjectWithoutFields(), JsonObjectWithoutFields())

        with self.assertRaises(ConfigurationError):
            Serializer.to_json_dict(self._container)

    def test_tuple_with_not_serializable_object(self):
        self._container.container = (NotSerializableObject(), NotSerializableObject())

        with self.assertRaises(TypeError):
            Serializer.to_json_dict(self._container)

    def test_tuple_with_list(self):
        self._container.container = (
            [],
            [1, 2, 3, 4],
            ["some string", "another string", "and yet another string"]
        )
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_tuple(self):
        self._container.container = (
            tuple([]),
            tuple([1, 2, 3, 4]),
            tuple(["some string", "another string"])
        )
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [list(item) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_set(self):
        self._container.container = (
            set([]),
            {1, 2, 3, 4, 5},
            {Container(), Container(), Container()},
            {"some string", "another string"}
        )
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [list(item) for item in self._container.container]
        for lst in expected:
            for i, item in enumerate(lst):
                if type(item) is Container:
                    lst[i] = Serializer.to_json_dict(lst[i])

        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_dict(self):
        self._container.container = (
            {},
            {"key1": "some string", "key2": "another string"},
            {"key1": 1, "key2": 2, "key3": 3}
        )
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_empty_set(self):
        self._container.container = set([])
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_set_with_none(self):
        self._container.container = {None, None, None}
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_set_with_str(self):
        self._container.container = {"some string", "string", "another string", "ayyyyyy"}
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_set_with_int(self):
        self._container.container = {1, 2, 3, 4, 5, 6}
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_set_with_float(self):
        self._container.container = {1.1, 2.1337, 3.42, 12.9999}
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = list(self._container.container)
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_set_with_json_object(self):
        self._container.container = {Container(), Container(), Container()}
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [Serializer.to_json_dict(item) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_set_with_json_object_without_fields(self):
        self._container.container = {JsonObjectWithoutFields(), JsonObjectWithoutFields()}

        with self.assertRaises(ConfigurationError):
            Serializer.to_json_dict(self._container)

    def test_set_with_not_serializable_object(self):
        self._container.container = {NotSerializableObject()}

        with self.assertRaises(TypeError):
            Serializer.to_json_dict(self._container)

    def test_set_with_tuple(self):
        self._container.container = {
            (),
            (1, 2, 3),
            ("a string", "str", "some string", "another string")
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [list(item) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_empty_dict(self):
        self._container.container = {}
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict
        self.assertDictEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_none(self):
        self._container.container = {
            "key1": None,
            "key2": None
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict
        self.assertDictEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_str(self):
        self._container.container = {
            "key1": "some string",
            "key2": "another string"
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict
        self.assertDictEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_int(self):
        self._container.container = {
            "key1": 1,
            "key2": 2,
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict
        self.assertDictEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_float(self):
        self._container.container = {
            "key1": 1.1337,
            "key2": 42.4444
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict
        self.assertDictEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_json_object(self):
        self._container.container = {
            "key1": Container(),
            "key2": Container()
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict

        expected = {
            key: Serializer.to_json_dict(self._container.container[key]) for key in self._container.container.keys()
        }
        self.assertDictEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_json_object_without_fields(self):
        self._container.container = {
            "key1": JsonObjectWithoutFields(),
            "key2": JsonObjectWithoutFields()
        }

        with self.assertRaises(ConfigurationError):
            Serializer.to_json_dict(self._container)

    def test_dict_with_not_serializable_object(self):
        self._container.container = {
            "key1": NotSerializableObject(),
            "key2": NotSerializableObject()
        }

        with self.assertRaises(TypeError):
            Serializer.to_json_dict(self._container)

    def test_dict_with_list(self):
        self._container.container = {
            "key1": [],
            "key2": ["some string", "another string"]
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict
        self.assertDictEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_tuple(self):
        self._container.container = {
            "key1": (),
            "key2": (1, 2, 3),
            "key3": ("s", "i", "p")
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict

        expected = {key: list(self._container.container[key]) for key in self._container.container.keys()}
        self.assertDictEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_set(self):
        self._container.container = {
            "key1": set([]),
            "key2": {1.1337, 42.0}
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict

        expected = {key: list(self._container.container[key]) for key in self._container.container.keys()}
        self.assertDictEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_dict(self):
        self._container.container = {
            "key1": {
                "key1": "string"
            },
            "key2": {
                "key1": 1,
                "key2": 2
            }
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict
        self.assertDictEqual(self._container.container, actual[Container.CONTAINER_FIELD_NAME])

    def test_inheritance(self):
        self._container.container = ExtendedCar()
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict
        self.assertIn(ExtendedCar.FIELD_MAX_SPEED_NAME, actual[Container.CONTAINER_FIELD_NAME].keys())
        self.assertIn(ExtendedCar.FIELD_MODEL_NAME_NAME, actual[Container.CONTAINER_FIELD_NAME].keys())
        self.assertIn(ExtendedCar.FIELD_HORSEPOWER_NAME, actual[Container.CONTAINER_FIELD_NAME].keys())


class DictSerializationWithTimes(unittest.TestCase):
    def setUp(self):
        self._container = Container()

    def test_date(self):
        date = datetime.date.today()
        self._container.container = date
        actual = Serializer.to_json_dict(self._container)

        expected = date.strftime(DATE_FORMAT)
        self.assertEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_with_naive_datetime(self):
        dt = datetime.datetime.now()
        self._container.container = dt
        actual = Serializer.to_json_dict(self._container)

        expected = dt.strftime(DATETIME_FORMAT)
        self.assertEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_with_utc_datetime(self):
        self._datetime_timezone_helper("UTC", "+0000")

    def test_with_berlin_datetime(self):
        self._datetime_timezone_helper("Europe/Berlin", "+0200")

    def test_with_london_datetime(self):
        self._datetime_timezone_helper("Europe/London", "+0100")

    def test_with_istanbul_datetime(self):
        self._datetime_timezone_helper("Europe/Istanbul", "+0300")

    def test_with_tokyo_datetime(self):
        self._datetime_timezone_helper("Asia/Tokyo", "+0900")

    def test_with_new_york_datetime(self):
        self._datetime_timezone_helper("America/New_York", get_new_york_utc_offset())

    def _datetime_timezone_helper(self, timezone_name, utc_offset):
        dt = datetime.datetime.now(tz.gettz(timezone_name))
        self._container.container = dt
        actual = Serializer.to_json_dict(self._container)

        expected = dt.strftime(DATETIME_TZ_FORMAT)
        self.assertEqual(expected, actual[Container.CONTAINER_FIELD_NAME])
        self.assertTrue(actual[Container.CONTAINER_FIELD_NAME].endswith(utc_offset))

    def test_list_with_date(self):
        self._container.container = [datetime.date.today(), datetime.date.today() - datetime.timedelta(1)]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [item.strftime(DATE_FORMAT) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_naive_datetime(self):
        self._container.container = [datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(1)]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [item.strftime(DATETIME_FORMAT) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_list_with_utc_datetime(self):
        self._datetime_timezone_list_helper("UTC", "+0000")

    def test_list_with_berlin_datetime(self):
        self._datetime_timezone_list_helper("Europe/Berlin", "+0200")

    def test_list_with_london_datetime(self):
        self._datetime_timezone_list_helper("Europe/London", "+0100")

    def test_list_with_istanbul_datetime(self):
        self._datetime_timezone_list_helper("Europe/Istanbul", "+0300")

    def test_list_with_tokyo_datetime(self):
        self._datetime_timezone_list_helper("Asia/Tokyo", "+0900")

    def test_list_with_new_york_datetime(self):
        self._datetime_timezone_list_helper("America/New_York", get_new_york_utc_offset())

    def _datetime_timezone_list_helper(self, timezone_name, utc_offset):
        self._container.container = [
            datetime.datetime.now(tz.gettz(timezone_name)),
            datetime.datetime.now(tz.gettz(timezone_name)) - datetime.timedelta(2),
            datetime.datetime.now(tz.gettz(timezone_name)) - datetime.timedelta(hours=5)
        ]
        self._datetime_timezone_iterable_helper(utc_offset)

    def test_tuple_with_date(self):
        self._container.container = (datetime.date.today(), datetime.date.today() - datetime.timedelta(1))
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [item.strftime(DATE_FORMAT) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_naive_datetime(self):
        self._container.container = [datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(hours=3)]
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [item.strftime(DATETIME_FORMAT) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_tuple_with_utc_datetime(self):
        self._datetime_timezone_tuple_helper("UTC", "+0000")

    def test_tuple_with_berlin_datetime(self):
        self._datetime_timezone_tuple_helper("Europe/Berlin", "+0200")

    def test_tuple_with_london_datetime(self):
        self._datetime_timezone_tuple_helper("Europe/London", "+0100")

    def test_tuple_with_istanbul_datetime(self):
        self._datetime_timezone_tuple_helper("Europe/Istanbul", "+0300")

    def test_tuple_with_tokyo_datetime(self):
        self._datetime_timezone_tuple_helper("Asia/Tokyo", "+0900")

    def test_tuple_with_new_york_datetime(self):
        self._datetime_timezone_tuple_helper("America/New_York", get_new_york_utc_offset())

    def _datetime_timezone_tuple_helper(self, timezone_name, utc_offset):
        self._container.container = (
            datetime.datetime.now(tz.gettz(timezone_name)),
            datetime.datetime.now(tz.gettz(timezone_name)) + datetime.timedelta(2),
            datetime.datetime.now(tz.gettz(timezone_name)) - datetime.timedelta(16)
        )
        self._datetime_timezone_iterable_helper(utc_offset)

    def test_set_with_date(self):
        self._container.container = {datetime.date.today()}
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [item.strftime(DATE_FORMAT) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_set_with_naive_datetime(self):
        self._container.container = {
            datetime.datetime.now(),
            datetime.datetime.now() - datetime.timedelta(1),
            datetime.datetime.now() - datetime.timedelta(hours=1)
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [item.strftime(DATETIME_FORMAT) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_set_with_utc_datetime(self):
        self._datetime_timezone_set_helper("UTC", "+0000")

    def test_set_with_berlin_datetime(self):
        self._datetime_timezone_set_helper("Europe/Berlin", "+0200")

    def test_set_with_london_datetime(self):
        self._datetime_timezone_set_helper("Europe/London", "+0100")

    def test_set_with_istanbul_datetime(self):
        self._datetime_timezone_set_helper("Europe/Istanbul", "+0300")

    def test_set_with_tokyo_datetime(self):
        self._datetime_timezone_set_helper("Asia/Tokyo", "+0900")

    def test_set_with_new_york_datetime(self):
        self._datetime_timezone_set_helper("America/New_York", get_new_york_utc_offset())

    def _datetime_timezone_set_helper(self, timezone_name, utc_offset):
        self._container.container = {
            datetime.datetime.now(tz.gettz(timezone_name)) - datetime.timedelta(7),
            datetime.datetime.now(tz.gettz(timezone_name)) + datetime.timedelta(hours=1),
            datetime.datetime.now(tz.gettz(timezone_name))
        }
        self._datetime_timezone_iterable_helper(utc_offset)

    def test_dict_with_date(self):
        self._container.container = {
            "key1": datetime.date.today(),
            "key2": datetime.date.today() - datetime.timedelta(7),
            "key3": datetime.date.today() - datetime.timedelta(39)
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict

        expected = {
            key: self._container.container[key].strftime(DATE_FORMAT) for key in self._container.container.keys()
        }
        self.assertDictEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_naive_datetime(self):
        self._container.container = {
            "key1": datetime.datetime.now() - datetime.timedelta(12)
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict

        expected = {
            key: self._container.container[key].strftime(DATETIME_FORMAT) for key in self._container.container.keys()
        }
        self.assertDictEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

    def test_dict_with_utc_datetime(self):
        self._datetime_timezone_dict_helper("UTC", "+0000")

    def test_dict_with_berlin_datetime(self):
        self._datetime_timezone_dict_helper("Europe/Berlin", "+0200")

    def test_dict_with_london_datetime(self):
        self._datetime_timezone_dict_helper("Europe/London", "+0100")

    def test_dict_with_istanbul_datetime(self):
        self._datetime_timezone_dict_helper("Europe/Istanbul", "+0300")

    def test_dict_with_tokyo_datetime(self):
        self._datetime_timezone_dict_helper("Asia/Tokyo", "+0900")

    def test_dict_with_new_york_datetime(self):
        self._datetime_timezone_dict_helper("America/New_York", get_new_york_utc_offset())

    def _datetime_timezone_dict_helper(self, timezone_name, utc_offset):
        self._container.container = {
            "key1": datetime.datetime.now(tz.gettz(timezone_name)) - datetime.timedelta(12),
            "key2": datetime.datetime.now(tz.gettz(timezone_name)),
            "key3": datetime.datetime.now(tz.gettz(timezone_name)) + datetime.timedelta(minutes=1)
        }
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is dict

        expected = {
            key: self._container.container[key].strftime(DATETIME_TZ_FORMAT) for key in self._container.container.keys()
        }
        self.assertDictEqual(expected, actual[Container.CONTAINER_FIELD_NAME])
        for key in actual[Container.CONTAINER_FIELD_NAME].keys():
            assert actual[Container.CONTAINER_FIELD_NAME][key].endswith(utc_offset)

    def _datetime_timezone_iterable_helper(self, utc_offset):
        actual = Serializer.to_json_dict(self._container)

        assert type(actual[Container.CONTAINER_FIELD_NAME]) is list

        expected = [item.strftime(DATETIME_TZ_FORMAT) for item in self._container.container]
        self.assertListEqual(expected, actual[Container.CONTAINER_FIELD_NAME])

        for item in actual[Container.CONTAINER_FIELD_NAME]:
            assert item.endswith(utc_offset)


class DictSerializationWithNotNullable(unittest.TestCase):
    def test_not_nullable_field_which_is_null(self):
        json_object = JsonObjectWithNotNullableField()
        json_object.not_nullable = None

        with self.assertRaises(FieldValidationError):
            Serializer.to_json_dict(json_object)

    def test_referenced_json_object_with_not_nullable_field_which_is_null(self):
        container = Container()
        container.container = JsonObjectWithNotNullableField()
        container.container.not_nullable = None

        with self.assertRaises(FieldValidationError):
            Serializer.to_json_dict(container)

    def test_list_with_json_object_with_not_nullable_field_which_is_null(self):
        json_object = JsonObjectWithNotNullableField()
        json_object.not_nullable = None

        container = Container()
        container.container = [json_object]

        with self.assertRaises(FieldValidationError):
            Serializer.to_json_dict(container)

    def test_tuple_with_json_object_with_not_nullable_field_which_is_null(self):
        json_object = JsonObjectWithNotNullableField()
        json_object.not_nullable = None

        container = Container()
        container.container = (json_object,)

        with self.assertRaises(FieldValidationError):
            Serializer.to_json_dict(container)

    def test_set_with_json_object_with_not_nullable_field_which_is_null(self):
        json_object = JsonObjectWithNotNullableField()
        json_object.not_nullable = None

        container = Container()
        container.container = {json_object,}

        with self.assertRaises(FieldValidationError):
            Serializer.to_json_dict(container)

    def test_dict_with_json_object_with_not_nullable_field_which_is_null(self):
        json_object = JsonObjectWithNotNullableField()
        json_object.not_nullable = None

        container = Container()
        container.container = {
            "key1": json_object
        }

        with self.assertRaises(FieldValidationError):
            Serializer.to_json_dict(container)
