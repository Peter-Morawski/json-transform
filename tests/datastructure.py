# -*- coding: utf-8 -*-

import pytz
import datetime
from jsontransform import JsonObject, field
from decorator import decorator


@decorator
def some_decorator(func, *args, **kwargs):
    if not hasattr(func, "_was_wrapped_with_some_decorator"):
        func._was_wrapped_with_some_decorator = True

    return func(*args, **kwargs)


class Color(JsonObject):
    FIELD_R_NAME = "r"
    FIELD_G_NAME = "g"
    FIELD_B_NAME = "b"
    DEFAULT_VALUE = 255

    def __init__(self):
        self._r = self.DEFAULT_VALUE
        self._g = self.DEFAULT_VALUE
        self._b = self.DEFAULT_VALUE

    @property
    @field()
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        self._r = value

    @property
    @field()
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        self._g = value

    @property
    @field()
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value


class Person(JsonObject):
    FIELD_FIRST_NAME = "FirstName"
    FIELD_LAST_NAME = "LastName"
    FIELD_HAIR_COLOR_NAME = "hairColor"
    FIELD_AGE_NAME = "age"
    FIELD_HEIGHT_NAME = "height"
    FIELD_FAVORITE_COLOR_NAME = "favoriteColor"
    FIELD_RELATIVES_NAME = "Relatives"
    FIELD_FRIENDS_NAMES_NAME = "friendNames"
    FIELD_FAVORITE_NUMBERS_NAME = "favoriteNumbers"
    FIELD_ACHIEVEMENTS_NAME = "achievements"
    FIELD_FAVORITE_PET_NAME = "favoritePet"
    FIELD_DICT_TYPE_NAME = "dictType"
    FIELD_BIRTH_DATE = "BirthDate"
    FIELD_RECORD_CREATED_NAME = "recordCreated"

    def __init__(self):
        self._first_name = ""
        self._last_name = ""
        self._hair_color = Color()
        self._age = 0
        self._height = 0.0
        self._favorite_color = None
        self._relatives = []
        self._friends_names = []
        self._favorite_numbers = []
        self._achievements = []
        self._favorite_pet = ""
        self._dict_type = {}
        self._birth_date = datetime.date.today()
        self._record_created = datetime.datetime.now(pytz.utc)

    @property
    @field(FIELD_FIRST_NAME)
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    @some_decorator
    @field(FIELD_LAST_NAME)
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    @field(FIELD_HAIR_COLOR_NAME)
    def hair_color(self):
        return self._hair_color

    @hair_color.setter
    def hair_color(self, value):
        self._hair_color = value

    @property
    @field()
    def age(self):
        # we don't set the name on this field to tests if the function name is used.
        return self._age

    @age.setter
    def age(self, value):
        self._age = value

    @property
    @field()
    def height(self):
        # we don't set the name on this field to tests if the function name is used.
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    @field(FIELD_FAVORITE_COLOR_NAME)
    def favorite_color(self):
        return self._favorite_color

    @favorite_color.setter
    def favorite_color(self, value):
        self._favorite_color = value

    @property
    @field(FIELD_RELATIVES_NAME)
    def relatives(self):
        return self._relatives

    @relatives.setter
    def relatives(self, value):
        self._relatives = value

    @property
    @field(FIELD_FRIENDS_NAMES_NAME)
    def friends_names(self):
        return self._friends_names

    @friends_names.setter
    def friends_names(self, value):
        self._friends_names = value

    @property
    @field(FIELD_FAVORITE_NUMBERS_NAME)
    def favorite_numbers(self):
        return self._favorite_numbers

    @favorite_numbers.setter
    def favorite_numbers(self, value):
        self._favorite_numbers = value

    @property
    @field()
    def achievements(self):
        return self._achievements

    @achievements.setter
    def achievements(self, value):
        self._achievements = value

    @property
    @field(FIELD_FAVORITE_PET_NAME)
    @some_decorator
    def favorite_pet(self):
        return self._favorite_pet

    @favorite_pet.setter
    def favorite_pet(self, value):
        self._favorite_pet = value

    @property
    @field(FIELD_DICT_TYPE_NAME)
    def dict_type(self):
        return self._dict_type

    @dict_type.setter
    def dict_type(self, value):
        self._dict_type = value

    @property
    @field(FIELD_BIRTH_DATE)
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = value

    @property
    @field(FIELD_RECORD_CREATED_NAME)
    def record_created(self):
        return self._record_created

    @record_created.setter
    def record_created(self, value):
        self._record_created = value


class PersonWithoutJsonField(JsonObject):
    def __init__(self):
        self._first_name = ""
        self._last_name = ""

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    @some_decorator
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value


class Achievement(JsonObject):
    FIELD_PLACE_NAME = "place"
    FIELD_MESSAGE_NAME = "message"

    def __init__(self):
        self._place = 0
        self._message = ""

    @property
    @field()
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        self._place = value

    @property
    @field()
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value


class AchievementWithoutFields(JsonObject):
    def __init__(self):
        self._place = 0
        self._message = 0

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        self._place = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value


class NotSerializableObject(object):
    def __init__(self):
        self._name = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class TimeObject(JsonObject):
    FIELD_DT_NAME = "datetime"
    FIELD_DATE_NAME = "date"

    def __init__(self):
        self._dt = datetime.datetime.now(pytz.utc)
        self._date = datetime.date.today()

    @property
    @field(FIELD_DT_NAME)
    def dt(self):
        return self._dt

    @dt.setter
    def dt(self, value):
        self._dt = value

    @property
    @field(FIELD_DATE_NAME)
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value


class Car(JsonObject):
    FIELD_MODEL_NAME_NAME = "modelName"
    FIELD_MAX_SPEED_NAME = "maxSpeed"

    def __init__(self):
        self._model_name = ""
        self._max_speed = 0

    @property
    @field(FIELD_MODEL_NAME_NAME)
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, value):
        self._model_name = value

    @property
    @field(FIELD_MAX_SPEED_NAME)
    def max_speed(self):
        return self._max_speed

    @max_speed.setter
    def max_speed(self, value):
        self._max_speed = value


class ExtendedCar(Car):
    FIELD_HORSEPOWER_NAME = "horsepower"

    def __init__(self):
        super(ExtendedCar, self).__init__()
        self._horsepower = 0

    @property
    @field()
    def horsepower(self):
        return self._horsepower

    @horsepower.setter
    def horsepower(self, value):
        self._horsepower = value
