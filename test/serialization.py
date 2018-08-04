# -*- coding: utf-8 -*-

import pytz
import unittest
import datetime
from datastructure import Person, Color, Achievement, AchievementWithoutFields, NotSerializableObject
from jsontransform import ConfigurationError, DATE_FORMAT, DATETIME_FORMAT, DATETIME_TZ_FORMAT, JsonObject

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


# TODO: Test list with other lists in it


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
        self.skipTest("Needs to be implemented")

    def test_type_list_with_dict(self):
        self.skipTest("Needs to be implemented")

    def test_type_list_with_set(self):
        self.skipTest("Needs to be implemented")

    def test_type_list_with_tuple(self):
        self.skipTest("Needs to be implemented")

    def test_type_list_with_json_object_without_field(self):
        self._john.achievements = [AchievementWithoutFields()]

        with self.assertRaises(ConfigurationError):
            self._john.to_json_dict()

    def test_type_list_with_not_serializable_object(self):
        self._john.achievements = [NotSerializableObject()]

        with self.assertRaises(TypeError):
            self._john.to_json_dict()

    def test_type_dict_with_str(self):
        self.skipTest("Needs to be implemented")

    def test_type_dict_with_int(self):
        self.skipTest("Needs to be implemented")

    def test_type_dict_with_float(self):
        self.skipTest("Needs to be implemented")

    def test_type_dict_with_none(self):
        self.skipTest("Needs to be implemented")

    def test_type_dict_with_list(self):
        self.skipTest("Needs to be implemented")

    def test_type_dict_with_set(self):
        self.skipTest("Needs to be implemented")

    def test_type_dict_with_tuple(self):
        self.skipTest("Needs to be implemented")

    def test_type_dict_with_not_serializable_object(self):
        self.skipTest("Needs to be implemented")

    def test_type_dict_with_json_object(self):
        self.skipTest("Needs to be implemented")

    def test_type_set(self):
        self.skipTest("Needs to be implemented")

    def test_type_tuple(self):
        self.skipTest("Needs to be implemented")

    def test_with_some_decorator_before_field_decorator(self):
        actual = self._john.to_json_dict()
        assert Person.FIELD_LAST_NAME in actual.keys()

    def test_with_some_decorator_after_field_decorator(self):
        actual = self._john.to_json_dict()
        assert Person.FIELD_FAVORITE_PET_NAME in actual.keys()

# class DictSerializationWithDates(unittest.TestCase):
#     def setUp(self):
#         self._person = PersonWithTimestamp()
#         self._person.first_name = JOHN_FIRST_NAME
#         self._person.last_name = JOHN_LAST_NAME
#         self._person.age = JOHN_AGE
#         self._expected_person = {
#             PersonWithTimestamp.FIELD_FIRST_NAME: JOHN_FIRST_NAME,
#             PersonWithTimestamp.FIELD_LAST_NAME: JOHN_LAST_NAME,
#             PersonWithTimestamp.FIELD_AGE_NAME: JOHN_AGE,
#             PersonWithTimestamp.FIELD_RELATIVES_NAME: [],
#         }
#
#     def test_to_json_dict_with_naive_datetime(self):
#         dt = datetime.datetime.now()
#         self._person.created = dt
#
#         self._expected_person[PersonWithTimestamp.FIELD_CREATED_NAME] = dt.strftime(DATETIME_FORMAT)
#         self.assertDictEqual(self._expected_person, self._person.to_json_dict())
#
#     def test_to_json_dict_with_utc_datetime(self):
#         self._datetime_timezone_helper("UTC", "+0000")
#
#     def test_to_json_dict_with_berlin_datetime(self):
#         self._datetime_timezone_helper("Europe/Berlin", "+0200")
#
#     def test_to_json_dict_with_london_datetime(self):
#         self._datetime_timezone_helper("Europe/London", "+0100")
#
#     def test_to_json_dict_with_istanbul_datetime(self):
#         self._datetime_timezone_helper("Europe/Istanbul", "+0300")
#
#     def test_to_json_dict_with_japan_datetime(self):
#         self._datetime_timezone_helper("Asia/Tokyo", "+0900")
#
#     def _datetime_timezone_helper(self, timezone_name, utc_offset):
#         dt = datetime.datetime.now(pytz.timezone(timezone_name))
#         self._person.created = dt
#
#         self._expected_person[PersonWithTimestamp.FIELD_CREATED_NAME] = dt.strftime(DATETIME_TZ_FORMAT)
#         self.assertDictEqual(self._expected_person, self._person.to_json_dict())
#         self.assertTrue(self._person.to_json_dict()[PersonWithTimestamp.FIELD_CREATED_NAME].endswith(utc_offset))
