# -*- coding: utf-8 -*-

import json
import inspect
import datetime
import collections
from decorator import decorator

DATE_FORMAT = "%Y-%m-%d"
DATETIME_TZ_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

_JSON_FIELD_NAME = "_json_field_name"


class ConfigurationError(Exception):
    pass


@decorator
def field(func, field_name=None, *args, **kwargs):
    """
    Decorator to mark a property getter inside a class (which must inherit from :class:`JsonObject`) as a field that
    can be serialized to a JSON object and deserialized from a JSON object.

    Usage Example
    =============

     class Person(JsonObject):
        def __init__(self):
            self._first_name = ""

        @property
        @field("FirstName")
        def first_name(self):
            return self._first_name

        @first_name.setter
        def first_name(self, value):
            self._first_name = value

    NOTE
    ====
    * The brackets `()` after the @field decorator are important even when no additional arguments are given
    * The :class:`property` decorator must be at the top or else the function won't be recognized as a property

    :param func: The property getter function (which is decorated with @property) that should be called to get
    the value for the JSON field.
    :param field_name: An optional name for the field. If this is not defined the the name of the property will be used.
    """
    if not hasattr(func, _JSON_FIELD_NAME):
        setattr(func, _JSON_FIELD_NAME, field_name or func.__name__)

    return func(*args, **kwargs)


class JsonObject(object):
    """
    A JsonObject is an object/class which is serializable into a JSON object and deserializable from a JSON object.
    It can be serialized into and deserialized from a

    * JSON string
    * JSON file
    * python dict
    """
    @classmethod
    def from_json_string(cls, json_string):
        """
        Deserialize a JSON string into an instance of this class.

        EXAMPLE
        =======
        JSON string = "{\"name\": \"Peter\", \"age\": 6}"

        class Person(JsonObject):
            def __init__(self):
                self._name = ""
                self._age = 0

            @property
            @field()
            def name(self):
                return self._name

            @name.setter
            def name(self, value):
                self._name = value

            @property
            @field()
            def age(self):
                return self._age

            @age.setter
            def age(self, value):
                self._age = value

        :param json_string: The string with the JSON object which should be deserialized into this object.
        :return: An instance of this class.
        """
        d = json.loads(json_string)
        return cls.from_json_dict(d)

    def to_json_string(self, encoding="utf-8"):
        """
        Serialize this object into a JSON string.

        :param encoding: The encoding of the string. Default utf-8
        :return: This object serialized as a JSON string.
        """
        return json.dumps(self.to_json_dict(), encoding=encoding)

    @classmethod
    def from_json_file(cls, f):
        """

        :param f:
        :return:
        """
        d = json.load(f)
        return cls.from_json_dict(d)

    def to_json_file(self, f, encoding="utf-8"):
        """
        Serialize this object into a file.

        :param f: a ``.write()``-supporting file-like object.
        :param encoding: The character encoding for str instances. Default utf-8
        """
        d = self.to_json_dict()
        json.dump(d, f, encoding=encoding)

    @classmethod
    def from_json_dict(cls, json_dict):
        """

        :param json_dict:
        :return:
        """
        result = cls()
        properties = _JsonUtil.get_decorated_properties(result)
        if not properties:
            raise ConfigurationError("The class doesn't define any fields which can be serialized into JSON")

        for p in properties.keys():
            value = _JsonUtil.get_normalized_property_value(json_dict.get(p))
            if value:
                properties[p].fset(result, value)

        return result

    def to_json_dict(self):
        """
        Serialize this object into a `dict`.

        :raises ConfigurationError: When this object doesn't define any property getter annotated with the ``field()``
        decorator.
        :return: The `dict` representation of this object.
        """
        result = {}
        properties = _JsonUtil.get_decorated_properties(self)
        if not properties.keys():
            raise ConfigurationError("The class doesn't define any fields which can be serialized into JSON")

        for key in properties.iterkeys():
            wrapper = properties[key].fget.__wrapped__
            property_value = properties[key].fget(self)

            property_name = _JsonUtil.get_json_field_name(wrapper)
            if property_name:
                result[property_name] = _JsonUtil.get_normalized_property_value(property_value)

        return result


JSONObject = JsonObject


class _JsonUtil(object):
    @classmethod
    def get_decorated_properties(cls, obj):
        """
        Get all properties from an object which are annotated with the ``field()`` decorator.

        :param obj: The instance of the object from which the properties should be extracted.
        :return: A `dict` containing all properties which are decorated with the :function:`field` decorator.
        In this `dict` the key is the name of the field (how it should appear in the JSON) and the value is the
        corresponding :class:`property`.
        """
        result = {}

        for member in inspect.getmembers(type(obj)):
            if type(member[1]) == property:
                if "__wrapped__" in member[1].fget.__dict__.keys():
                    member[1].fget(obj)
                    wrapper = member[1].fget.__wrapped__

                    if cls.get_json_field_name(wrapper):
                        result[cls.get_json_field_name(wrapper)] = member[1]

        return result

    @classmethod
    def get_json_field_name(cls, property_getter):
        """
        Get the Value of the _JSON_FIELD_NAME attribute of a property getter function.

        NOTE
        ====
        If the property getter is annotated with multiple decorators it will search all wrappers.

        :param property_getter: The function which should be checked for the _JSON_FIELD_NAME attribute.
        :return: The name of the JSON field; `None` otherwise.
        """
        if hasattr(property_getter, _JSON_FIELD_NAME):
            return getattr(property_getter, _JSON_FIELD_NAME)

        if "__wrapped__" in property_getter.__dict__.keys():
            return cls.get_json_field_name(property_getter.__wrapped__)

        return None

    @classmethod
    def get_normalized_property_value(cls, property_value):
        """
        Check if the value of a property is JSON serializable and if necessary transform it so that it can be
        serialized.

        :param property_value: The value of the property which should be checked and possibly transformed.
        :raises TypeError: When the type of the property value is not JSON serializable.
        :return: The normalized value of the property which can be serialized.
        """
        if property_value is None:
            return property_value
        elif cls.property_is_simple_type(property_value):
            return property_value
        elif isinstance(property_value, dict):
            result = {}
            for key in property_value.keys():
                result[key] = cls.get_normalized_property_value(property_value[key])

            return result
        elif cls.property_not_str_and_iterable(property_value):
            result = []
            for item in property_value:
                result.append(cls.get_normalized_property_value(item))

            return result
        elif isinstance(property_value, JsonObject):
            return property_value.to_json_dict()
        elif isinstance(property_value, datetime.datetime):
            if property_value.tzinfo:
                return property_value.strftime(DATETIME_TZ_FORMAT)
            else:
                return property_value.strftime(DATETIME_FORMAT)
        elif isinstance(property_value, datetime.date):
            return property_value.strftime(DATE_FORMAT)
        else:
            raise TypeError("The object type `{}` is not JSON serializable".format(type(property_value)))

    @classmethod
    def property_is_simple_type(cls, property_value):
        """
        Check if a property has a simple type which can be simply serialized without any further work.

        :param property_value: The property value which should be checked.
        :return: `True` if the properties value type is simple; `False` otherwise.
        """
        return (
            type(property_value) == str or
            type(property_value) == int or
            type(property_value) == float
        )

    @classmethod
    def property_not_str_and_iterable(cls, property_value):
        """
        Check if a property of a class is iterable and **NOT** a `str`.

        :param property_value: The property value which should be checked.
        :return: `True` if the property value is iterable and NOT a `str`; `False`otherwise.
        """
        return type(property_value) is not str and isinstance(property_value, collections.Iterable)

