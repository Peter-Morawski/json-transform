# -*- coding: utf-8 -*-

import pytz
import unittest
import datetime
from .datastructure import Person, Color, Achievement, AchievementWithoutFields, NotSerializableObject, TimeObject, \
    ExtendedCar
from jsontransform import ConfigurationError, DATE_FORMAT, DATETIME_FORMAT, DATETIME_TZ_FORMAT

JOHN_FIRST_NAME = "John"
JOHN_LAST_NAME = "Doe"
JOHN_AGE = 38
JOHN_BIRTH_DATE = datetime.date(1989, 9, 11)
JOHN_HEIGHT = 171.26
JOHN_FAVORITE_COLOR = None
JOHN_FRIENDS_NAMES = ["Dennis Ritchie", "Linus Torvalds", "Bill Gates", "Eric Schmidt"]
JOHN_FAVORITE_INT_NUMBERS = [42, 1337, 54153, 5556, 111328546]
JOHN_FAVORITE_FLOAT_NUMBERS = [37.658, 359.2524, 654685.123, .002, .2]

MOTHER_FIRST_NAME = "Richard"
MOTHER_LAST_NAME = "Doe"
MOTHER_AGE = 72
MOTHER_RELATIVES = []

FATHER_FIRST_NAME = "Catherine"
FATHER_LAST_NAME = "Doe"
FATHER_AGE = 17
FATHER_RELATIVES = []


class DictSerialization(unittest.TestCase):
    def setUp(self):
        self._mother = Person()
        self._mother.first_name = MOTHER_FIRST_NAME
        self._mother.last_name = MOTHER_LAST_NAME
        self._mother.age = MOTHER_AGE

        self._father = Person()
        self._father.first_name = FATHER_FIRST_NAME
        self._father.last_name = FATHER_LAST_NAME
        self._father.age = FATHER_AGE

        self._john = Person()
        self._john.first_name = JOHN_FIRST_NAME
        self._john.last_name = JOHN_LAST_NAME
        self._john.age = JOHN_AGE
        self._john.height = JOHN_HEIGHT
        self._john.favorite_color = JOHN_FAVORITE_COLOR
        self._john.relatives = [self._mother, self._father]
        self._john.friends_names = JOHN_FRIENDS_NAMES

    def test_custom_field_name(self):
        assert Person.FIELD_FIRST_NAME in self._john.to_json_dict().keys()

    def test_no_custom_field_name(self):
        assert Person.FIELD_AGE_NAME in self._john.to_json_dict().keys()

    def test_type_str(self):
        actual = self._john.to_json_dict()
        assert type(actual[Person.FIELD_FIRST_NAME]) is str
        assert JOHN_FIRST_NAME == actual[Person.FIELD_FIRST_NAME]

    def test_type_int(self):
        actual = self._john.to_json_dict()
        assert type(actual[Person.FIELD_AGE_NAME]) is int
        assert JOHN_AGE == actual[Person.FIELD_AGE_NAME]

    def test_type_float(self):
        actual = self._john.to_json_dict()
        assert type(actual[Person.FIELD_HEIGHT_NAME]) is float
        assert JOHN_HEIGHT == actual[Person.FIELD_HEIGHT_NAME]

    def test_type_json_object(self):
        actual = self._john.to_json_dict()
        field_hair_color = actual[Person.FIELD_HAIR_COLOR_NAME]

        assert type(field_hair_color) is dict
        assert Color.FIELD_R_NAME in field_hair_color.keys()
        assert Color.FIELD_G_NAME in field_hair_color.keys()
        assert Color.FIELD_B_NAME in field_hair_color.keys()
        assert field_hair_color[Color.FIELD_R_NAME] == Color.DEFAULT_VALUE
        assert field_hair_color[Color.FIELD_G_NAME] == Color.DEFAULT_VALUE
        assert field_hair_color[Color.FIELD_B_NAME] == Color.DEFAULT_VALUE

    def test_type_none(self):
        actual = self._john.to_json_dict()
        field_favorite_color = actual[Person.FIELD_FAVORITE_COLOR_NAME]

        assert field_favorite_color is None
        assert JOHN_FAVORITE_COLOR == field_favorite_color

    def test_not_serializable_type(self):
        self._john.hair_color = NotSerializableObject()
        with self.assertRaises(TypeError):
            self._john.to_json_dict()

    def test_type_list_with_str(self):
        actual = self._john.to_json_dict()
        field_friend_names = actual[Person.FIELD_FRIENDS_NAMES_NAME]

        assert type(field_friend_names) is list
        assert all(type(item) is str for item in field_friend_names)
        assert len(JOHN_FRIENDS_NAMES) == len(field_friend_names)
        for name in JOHN_FRIENDS_NAMES:
            assert name in field_friend_names

    def test_type_list_with_int(self):
        self._john.favorite_numbers = JOHN_FAVORITE_INT_NUMBERS
        actual = self._john.to_json_dict()
        field_favorite_numbers = actual[Person.FIELD_FAVORITE_NUMBERS_NAME]

        assert type(field_favorite_numbers) is list
        assert all(type(item) is int for item in field_favorite_numbers)
        assert len(JOHN_FAVORITE_INT_NUMBERS) == len(field_favorite_numbers)
        for number in JOHN_FAVORITE_INT_NUMBERS:
            assert number in field_favorite_numbers

    def test_type_list_with_float(self):
        self._john.favorite_numbers = JOHN_FAVORITE_FLOAT_NUMBERS
        actual = self._john.to_json_dict()
        field_favorite_numbers = actual[Person.FIELD_FAVORITE_NUMBERS_NAME]

        assert type(field_favorite_numbers) is list
        assert all(type(item) is float for item in field_favorite_numbers)
        assert len(JOHN_FAVORITE_FLOAT_NUMBERS) == len(field_favorite_numbers)
        for number in JOHN_FAVORITE_FLOAT_NUMBERS:
            assert number in field_favorite_numbers

    def test_type_list_with_json_object(self):
        actual = self._john.to_json_dict()
        field_relatives = actual[Person.FIELD_RELATIVES_NAME]

        assert type(field_relatives) is list
        assert all(type(item) is dict for item in field_relatives)
        assert len(field_relatives) == 2

        mother = field_relatives[0]
        assert mother[Person.FIELD_FIRST_NAME] == MOTHER_FIRST_NAME
        assert mother[Person.FIELD_LAST_NAME] == MOTHER_LAST_NAME
        assert mother[Person.FIELD_AGE_NAME] == MOTHER_AGE
        assert mother[Person.FIELD_RELATIVES_NAME] == MOTHER_RELATIVES

        father = field_relatives[1]
        assert father[Person.FIELD_FIRST_NAME] == FATHER_FIRST_NAME
        assert father[Person.FIELD_LAST_NAME] == FATHER_LAST_NAME
        assert father[Person.FIELD_AGE_NAME] == FATHER_AGE
        assert father[Person.FIELD_RELATIVES_NAME] == FATHER_RELATIVES

    def test_type_list_with_none(self):
        achievements = [None, None, None]
        self._john.achievements = achievements
        actual = self._john.to_json_dict()
        field_achievements = actual[Person.FIELD_ACHIEVEMENTS_NAME]

        assert type(field_achievements) is list
        assert all(item is None for item in field_achievements)
        assert len(field_achievements) == len(achievements)
        for achievement in achievements:
            assert achievement in field_achievements

    def test_type_list_with_list(self):
        achievements = [
            JOHN_FRIENDS_NAMES
        ]
        self._john.achievements = achievements
        actual = self._john.to_json_dict()
        field_achievements = actual[Person.FIELD_ACHIEVEMENTS_NAME]

        assert type(field_achievements) is list
        assert all(type(item) is list for item in field_achievements)
        assert len(field_achievements) == len(achievements)
        assert achievements[0] in field_achievements

    def test_type_list_with_dict(self):
        achievements = [
            {
                "key1": [1, 2, 3],
                "key2": None
            }
        ]
        self._john.achievements = achievements
        actual = self._john.to_json_dict()
        field_achievements = actual[Person.FIELD_ACHIEVEMENTS_NAME]

        assert type(field_achievements) is list
        assert all(type(item) is dict for item in field_achievements)
        assert len(field_achievements) == len(achievements)
        assert achievements[0] in field_achievements

    def test_type_list_with_set(self):
        achievements = [
            set(JOHN_FRIENDS_NAMES)
        ]
        self._john.achievements = achievements
        actual = self._john.to_json_dict()
        field_achievements = actual[Person.FIELD_ACHIEVEMENTS_NAME]

        assert type(field_achievements) is list
        assert all(type(item) is list for item in field_achievements)
        assert len(field_achievements) == len(achievements)
        assert list(achievements[0]) in field_achievements

    def test_type_list_with_tuple(self):
        achievements = [
            tuple(JOHN_FRIENDS_NAMES)
        ]
        self._john.achievements = achievements
        actual = self._john.to_json_dict()
        field_achievements = actual[Person.FIELD_ACHIEVEMENTS_NAME]

        assert type(field_achievements) is list
        assert all(type(item) is list for item in field_achievements)
        assert len(field_achievements) == len(achievements)
        assert list(achievements[0]) in field_achievements

    def test_type_list_with_json_object_without_field(self):
        self._john.achievements = [AchievementWithoutFields()]

        with self.assertRaises(ConfigurationError):
            self._john.to_json_dict()

    def test_type_list_with_not_serializable_object(self):
        self._john.achievements = [NotSerializableObject()]

        with self.assertRaises(TypeError):
            self._john.to_json_dict()

    def test_type_dict_with_str(self):
        dict_type = {
            "key": JOHN_FIRST_NAME
        }
        self._john.dict_type = dict_type
        actual = self._john.to_json_dict()
        field_dict_type = actual[Person.FIELD_DICT_TYPE_NAME]

        assert type(field_dict_type) is dict
        assert dict_type == field_dict_type

    def test_type_dict_with_int(self):
        dict_type = {
            "key": JOHN_AGE
        }
        self._john.dict_type = dict_type
        actual = self._john.to_json_dict()
        field_dict_type = actual[Person.FIELD_DICT_TYPE_NAME]

        assert type(field_dict_type) is dict
        assert dict_type == field_dict_type

    def test_type_dict_with_float(self):
        dict_type = {
            "key": JOHN_HEIGHT
        }
        self._john.dict_type = dict_type
        actual = self._john.to_json_dict()
        field_dict_type = actual[Person.FIELD_DICT_TYPE_NAME]

        assert type(field_dict_type) is dict
        assert dict_type == field_dict_type

    def test_type_dict_with_none(self):
        dict_type = {
            "key": None
        }
        self._john.dict_type = dict_type
        actual = self._john.to_json_dict()
        field_dict_type = actual[Person.FIELD_DICT_TYPE_NAME]

        assert type(field_dict_type) is dict
        assert dict_type == field_dict_type

    def test_type_dict_with_list(self):
        dict_type = {
            "key": JOHN_FRIENDS_NAMES
        }
        self._john.dict_type = dict_type
        actual = self._john.to_json_dict()
        field_dict_type = actual[Person.FIELD_DICT_TYPE_NAME]

        assert type(field_dict_type) is dict
        assert len(JOHN_FRIENDS_NAMES) == len(field_dict_type["key"])
        for name in JOHN_FRIENDS_NAMES:
            assert name in field_dict_type["key"]

    def test_type_dict_with_set(self):
        self._john.dict_type = {
            "key": set(JOHN_FRIENDS_NAMES)
        }
        actual = self._john.to_json_dict()
        field_dict_type = actual[Person.FIELD_DICT_TYPE_NAME]

        assert type(field_dict_type) is dict
        assert type(field_dict_type["key"]) is list
        assert len(JOHN_FRIENDS_NAMES) == len(field_dict_type["key"])
        for name in JOHN_FRIENDS_NAMES:
            assert name in field_dict_type["key"]

    def test_type_dict_with_tuple(self):
        self._john.dict_type = {
            "key": tuple(JOHN_FRIENDS_NAMES)
        }
        actual = self._john.to_json_dict()
        field_dict_type = actual[Person.FIELD_DICT_TYPE_NAME]

        assert type(field_dict_type) is dict
        assert type(field_dict_type["key"]) is list
        assert len(JOHN_FRIENDS_NAMES) == len(field_dict_type["key"])
        for name in JOHN_FRIENDS_NAMES:
            assert name in field_dict_type["key"]

    def test_type_dict_with_dict(self):
        self._john.dict_type = {
            "key": {
                "key": JOHN_FIRST_NAME
            }
        }
        actual = self._john.to_json_dict()
        field_dict_type = actual[Person.FIELD_DICT_TYPE_NAME]

        assert type(field_dict_type) is dict
        self.assertDictEqual(self._john.dict_type, field_dict_type)

    def test_type_dict_with_not_serializable_object(self):
        dict_type = {
            "key": NotSerializableObject()
        }
        self._john.dict_type = dict_type

        with self.assertRaises(TypeError):
            self._john.to_json_dict()

    def test_type_dict_with_json_object(self):
        dict_type = {
            "key": Achievement()
        }
        self._john.dict_type = dict_type
        actual = self._john.to_json_dict()
        field_dict_type = actual[Person.FIELD_DICT_TYPE_NAME]

        assert type(field_dict_type) is dict

        expected = {
            "key": Achievement().to_json_dict()
        }
        self.assertDictEqual(expected, field_dict_type)

    def test_if_type_set_is_converted_to_list(self):
        self._john.achievements = set(JOHN_FRIENDS_NAMES)
        actual = self._john.to_json_dict()
        assert type(actual[Person.FIELD_ACHIEVEMENTS_NAME]) is list

    def test_if_type_tuple_is_converted_to_list(self):
        self._john.achievements = tuple(JOHN_FRIENDS_NAMES)
        actual = self._john.to_json_dict()
        assert type(actual[Person.FIELD_ACHIEVEMENTS_NAME]) is list

    def test_with_some_decorator_before_field_decorator(self):
        actual = self._john.to_json_dict()
        assert Person.FIELD_LAST_NAME in actual.keys()

    def test_with_some_decorator_after_field_decorator(self):
        actual = self._john.to_json_dict()
        assert Person.FIELD_FAVORITE_PET_NAME in actual.keys()

    def test_if_inherits_fields(self):
        extended_car = ExtendedCar()
        actual = extended_car.to_json_dict()

        assert ExtendedCar.FIELD_HORSEPOWER_NAME in actual.keys()
        assert ExtendedCar.FIELD_MODEL_NAME_NAME in actual.keys()
        assert ExtendedCar.FIELD_MAX_SPEED_NAME in actual.keys()


class DictSerializationWithTimes(unittest.TestCase):
    def setUp(self):
        self._time_obj = TimeObject()

    def test_date(self):
        date = datetime.date.today()
        expected = date.strftime(DATE_FORMAT)

        self._time_obj.date = date
        actual = self._time_obj.to_json_dict()
        field_date = actual[TimeObject.FIELD_DATE_NAME]

        assert field_date == expected

    def test_with_naive_datetime(self):
        dt = datetime.datetime.now()
        expected = dt.strftime(DATETIME_FORMAT)

        self._time_obj.dt = dt
        actual = self._time_obj.to_json_dict()
        field_dt = actual[TimeObject.FIELD_DT_NAME]

        assert field_dt == expected

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

    def _datetime_timezone_helper(self, timezone_name, utc_offset):
        dt = datetime.datetime.now(pytz.timezone(timezone_name))
        self._time_obj.dt = dt

        expected = dt.strftime(DATETIME_TZ_FORMAT)
        actual = self._time_obj.to_json_dict()
        field_dt = actual[TimeObject.FIELD_DT_NAME]

        assert field_dt == expected
        self.assertTrue(field_dt.endswith(utc_offset))
