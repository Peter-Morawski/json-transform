# -*- coding: utf-8 -*-

import unittest
import datetime
from .datastructure import ExtendedCar, SimpleJsonObjectHolder, Color, Car, TimeObject

EXTENDED_CAR_DICT = {
    ExtendedCar.FIELD_MODEL_NAME_NAME: "some car model",
    ExtendedCar.FIELD_MAX_SPEED_NAME: 130,
    ExtendedCar.FIELD_HORSEPOWER_NAME: 30
}

SIMPLE_JSON_OBJECT_HOLDER_COLOR_DICT = {
    SimpleJsonObjectHolder.FIELD_INNER_JSON_OBJECT_NAME: {
        Color.FIELD_R_NAME: 125,
        Color.FIELD_G_NAME: 199,
        Color.FIELD_B_NAME: 16
    }
}

SIMPLE_JSON_OBJECT_HOLDER_UNKNOWN_INNER_DICT = {
    SimpleJsonObjectHolder.FIELD_INNER_JSON_OBJECT_NAME: {
    }
}

SIMPLE_JSON_OBJECT_HOLDER_NESTED_DICT = {
    SimpleJsonObjectHolder.FIELD_INNER_JSON_OBJECT_NAME: {
        SimpleJsonObjectHolder.FIELD_INNER_JSON_OBJECT_NAME: {
            SimpleJsonObjectHolder.FIELD_INNER_JSON_OBJECT_NAME: {
                Color.FIELD_R_NAME: 123,
                Color.FIELD_G_NAME: 200,
                Color.FIELD_B_NAME: 112
            }
        }
    }
}


class DictDeserialization(unittest.TestCase):
    def test_extended_car(self):
        extended_car = ExtendedCar.from_json_dict(EXTENDED_CAR_DICT)

        self.assertIsNotNone(extended_car)
        assert type(extended_car) is ExtendedCar
        assert extended_car.model_name == EXTENDED_CAR_DICT[ExtendedCar.FIELD_MODEL_NAME_NAME]
        assert extended_car.max_speed == EXTENDED_CAR_DICT[ExtendedCar.FIELD_MAX_SPEED_NAME]
        assert extended_car.horsepower == EXTENDED_CAR_DICT[ExtendedCar.FIELD_HORSEPOWER_NAME]

    def test_super_class_of_extended_car(self):
        car = Car.from_json_dict(EXTENDED_CAR_DICT)

        self.assertIsNotNone(car)
        assert type(car) is Car
        assert car.model_name == EXTENDED_CAR_DICT[Car.FIELD_MODEL_NAME_NAME]
        assert car.max_speed == EXTENDED_CAR_DICT[Car.FIELD_MAX_SPEED_NAME]

    def test_with_json_object(self):
        simple_json_object_holder = SimpleJsonObjectHolder.from_json_dict(SIMPLE_JSON_OBJECT_HOLDER_COLOR_DICT)

        self.assertIsNotNone(simple_json_object_holder)
        assert type(simple_json_object_holder) is SimpleJsonObjectHolder

        self.assertIsNotNone(simple_json_object_holder.inner_json_object)
        assert type(simple_json_object_holder.inner_json_object) is Color

        inner_json_object = SIMPLE_JSON_OBJECT_HOLDER_COLOR_DICT[SimpleJsonObjectHolder.FIELD_INNER_JSON_OBJECT_NAME]
        assert simple_json_object_holder.inner_json_object.r == inner_json_object[Color.FIELD_R_NAME]
        assert simple_json_object_holder.inner_json_object.g == inner_json_object[Color.FIELD_G_NAME]
        assert simple_json_object_holder.inner_json_object.b == inner_json_object[Color.FIELD_B_NAME]

    def test_with_wrong_dict(self):
        with self.assertRaises(TypeError):
            Color.from_json_dict(EXTENDED_CAR_DICT)

    def test_with_inner_unknown_dict(self):
        simple_json_object_holder = SimpleJsonObjectHolder.from_json_dict(SIMPLE_JSON_OBJECT_HOLDER_UNKNOWN_INNER_DICT)

        self.assertIsNotNone(simple_json_object_holder)
        assert type(simple_json_object_holder) is SimpleJsonObjectHolder

        self.assertIsNotNone(simple_json_object_holder.inner_json_object)
        assert type(simple_json_object_holder.inner_json_object) is dict

    def test_with_empty_dict(self):
        with self.assertRaises(TypeError):
            SimpleJsonObjectHolder.from_json_dict({})

    def test_nested_json_objects(self):
        simple_json_object_holder = SimpleJsonObjectHolder.from_json_dict(SIMPLE_JSON_OBJECT_HOLDER_NESTED_DICT)

        self.assertIsNotNone(simple_json_object_holder)
        assert type(simple_json_object_holder) is SimpleJsonObjectHolder

        inner = SimpleJsonObjectHolder.FIELD_INNER_JSON_OBJECT_NAME
        color_dict = SIMPLE_JSON_OBJECT_HOLDER_NESTED_DICT[inner][inner][inner]

        self.assertIsNotNone(simple_json_object_holder.inner_json_object)
        assert type(simple_json_object_holder.inner_json_object) is SimpleJsonObjectHolder

        self.assertIsNotNone(simple_json_object_holder.inner_json_object.inner_json_object)
        assert type(simple_json_object_holder.inner_json_object.inner_json_object) is SimpleJsonObjectHolder

        self.assertIsNotNone(simple_json_object_holder.inner_json_object.inner_json_object.inner_json_object)
        assert type(simple_json_object_holder.inner_json_object.inner_json_object.inner_json_object) is Color

        color = simple_json_object_holder.inner_json_object.inner_json_object.inner_json_object
        assert color.r == color_dict[Color.FIELD_R_NAME]
        assert color.g == color_dict[Color.FIELD_G_NAME]
        assert color.b == color_dict[Color.FIELD_B_NAME]


class DictDeserializationTimes(unittest.TestCase):
    def test_date(self):
        d = {
            TimeObject.FIELD_DATE_NAME: "2018-08-06"
        }
        time_object = TimeObject.from_json_dict(d)

        self.assertIsNotNone(time_object)
        assert type(time_object) is TimeObject

        self.assertIsNotNone(time_object.date)
        assert type(time_object.date) is datetime.date
        assert time_object.date.year == 2018
        assert time_object.date.month == 8
        assert time_object.date.day == 6

    def test_naive_datetime(self):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-08-06T18:00:00Z"
        }
        time_object = TimeObject.from_json_dict(d)

        self.assertIsNotNone(time_object)
        assert type(time_object) is TimeObject

        self.assertIsNotNone(time_object.dt)
        assert type(time_object.dt) is datetime.datetime
        assert time_object.dt.year == 2018
        assert time_object.dt.month == 8
        assert time_object.dt.day == 6
        assert time_object.dt.hour == 18
        assert time_object.dt.minute == 0
        assert time_object.dt.second == 0
        self.assertIsNone(time_object.dt.tzinfo)

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

    def test_broken_naive_datetime_without_year(self):
        d = {
            TimeObject.FIELD_DT_NAME: "08-06T18:00:00Z"
        }
        self._broken_timezone_datetime_helper(d)

    def test_broken_naive_datetime_without_month_or_day(self):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-06T18:00:00Z"
        }
        self._broken_timezone_datetime_helper(d)

    def test_broken_naive_datetime_without_time_separator(self):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-08-06 18:00:00Z"
        }
        self._broken_timezone_datetime_helper(d)

    def test_broken_naive_datetime_without_hour_minute_or_second(self):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-08-06T00:00Z"
        }
        self._broken_timezone_datetime_helper(d)

    def test_broken_naive_datetime_without_hour_separator(self):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-08-06T18:00:00"
        }
        self._broken_timezone_datetime_helper(d)

    def test_broken_datetime_broken_timezone_without_plus(self):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-08-06T18:00:00Z0000"
        }
        self._broken_timezone_datetime_helper(d)

    def test_broken_datetime_broken_timezone_1(self):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-08-06T18:00:00Z+000"
        }
        self._broken_timezone_datetime_helper(d)

    def test_broken_datetime_broken_timezone_2(self):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-08-06T18:00:00Z+00"
        }
        self._broken_timezone_datetime_helper(d)

    def test_broken_datetime_broken_timezone_3(self):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-08-06T18:00:00Z+0"
        }
        self._broken_timezone_datetime_helper(d)

    def test_broken_datetime_broken_timezone_only_plus(self):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-08-06T18:00:00Z+"
        }
        self._broken_timezone_datetime_helper(d)

    def _datetime_timezone_helper(self, utc_offset, utc_offset_int):
        d = {
            TimeObject.FIELD_DT_NAME: "2018-08-06T18:00:00" + utc_offset
        }
        time_object = TimeObject.from_json_dict(d)

        self.assertIsNotNone(time_object)
        assert type(time_object) is TimeObject

        self.assertIsNotNone(time_object.dt)
        assert type(time_object.dt) is datetime.datetime
        assert time_object.dt.year == 2018
        assert time_object.dt.month == 8
        assert time_object.dt.day == 6
        assert time_object.dt.hour == 18
        assert time_object.dt.minute == 0
        assert time_object.dt.second == 0
        self.assertIsNotNone(time_object.dt.tzinfo)

        offset_seconds = time_object.dt.tzinfo.utcoffset(time_object.dt).seconds
        assert (offset_seconds if offset_seconds == 0 else (offset_seconds / 60) / 60) == utc_offset_int

    def _broken_timezone_datetime_helper(self, time_object_dict):
        time_object = TimeObject.from_json_dict(time_object_dict)

        self.assertIsNotNone(time_object)
        assert type(time_object) is TimeObject

        self.assertIsNotNone(time_object.dt)
        assert type(time_object.dt) is str
