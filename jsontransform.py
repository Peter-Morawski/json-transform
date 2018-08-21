# -*- coding: utf-8 -*-

import re
import json
import inspect
import datetime
import collections
from decorator import decorator
from dateutil import parser

DATE_FORMAT = "%Y-%m-%d"
DATETIME_TZ_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

_DATE_FORMAT_REGEX = r"^[0-9]{4}-[0-9]{1,}-[0-9]{1,}$"
_DATETIME_TZ_FORMAT_REGEX = r"^[0-9]{4}-[0-9]{1,}-[0-9]{1,}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\+|\-)[0-9]{4}$"
_DATETIME_FORMAT_REGEX = r"^[0-9]{4}-[0-9]{1,}-[0-9]{1,}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"

_JSON_FIELD_NAME = "_json_field_name"
_JSON_FIELD_REQUIRED = "_json_field_required"
_JSON_FIELD_NULLABLE = "_json_field_nullable"


class ConfigurationError(Exception):
    pass


class FieldValidationError(Exception):
    pass


class MissingObjectError(Exception):
    pass


@decorator
def field(func, field_name=None, required=False, nullable=True, *args, **kwargs):
    """
    Decorator to mark a property getter inside a class (which must inherit from :class:`JsonObject`) as a field that
    can be serialized to a JSON object and deserialized from a JSON object.

    Usage Example
    =============

     class Person(JsonObject):
        def __init__(self):
            self._first_name = ""

        @property
        @field("firstName")
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
    :param field_name: An optional name for the field. If this is not defined the the name of the property getter will
    be used.
    :param required: Indicates if this field is required which just applies for the deserialization.
    :param nullable: Indicates if the value of this field can be `None` which will be validated during serialization
    and deserialization.
    """
    if not hasattr(func, _JSON_FIELD_NAME):
        setattr(func, _JSON_FIELD_NAME, field_name or func.__name__)
    if not hasattr(func, _JSON_FIELD_REQUIRED):
        setattr(func, _JSON_FIELD_REQUIRED, required)
    if not hasattr(func, _JSON_FIELD_NULLABLE):
        setattr(func, _JSON_FIELD_NULLABLE, nullable)

    return func(*args, **kwargs)


class JsonObject(object):
    """
    A JsonObject is an object/class which is serializable into a JSON object and deserializable from a JSON object.
    """
    pass


JSONObject = JsonObject


class Serializer(object):
    """
    Provides functions to serialize a :class:`JsonObject` into:

    * an `str`
    * a file-like object
    * a `dict`
    """
    @classmethod
    def to_json_string(cls, json_object):
        """
        Serialize a :class:`JsonObject` into an `str`.

        :param json_object: The `JsonObject` which should be serialized.
        :return: A `str` which contains the serialized `JsonObject`.
        :raises ConfigurationError: When the given `JsonObject` doesn't define any fields.
        :raises FieldValidationError: When a field constraint has been violated e.g. a required field is missing.
        :raises TypeError: When a field in the given `JsonObject` couldn't be serialized.
        """
        return json.dumps(cls.to_json_dict(json_object))

    @classmethod
    def to_json_file(cls, json_file, json_object):
        """
        Serialize a :class:`JsonObject` into a file.

        :param json_file: A `write()`-supporting file-like object.
        :param json_object: The `JsonObject` which should be serialized.
        :raises ConfigurationError: When the given `JsonObject` doesn't define any fields.
        :raises FieldValidationError: When a field constraint has been violated e.g. a required field is missing.
        :raises TypeError: When a field in the given `JsonObject` couldn't be serialized.
        """
        json.dump(cls.to_json_dict(json_object), json_file)

    @classmethod
    def to_json_dict(cls, json_object):
        """
        Serialize a :class:`JsonObject` into a `dict`.

        :param json_object: The `JsonObject` which should be serialized.
        :return: A `dict` which represents the `JsonObject`.
        :raises ConfigurationError: When the given `JsonObject` doesn't define any fields.
        :raises FieldValidationError: When a field constraint has been violated e.g. a required field is missing.
        :raises TypeError: When a field in the given `JsonObject` couldn't be serialized.
        """
        result = {}
        properties = _JsonCommon.get_decorated_properties(json_object)
        if not properties.keys():
            raise ConfigurationError("The class doesn't define any fields which can be serialized into JSON")

        _JsonValidation.validate_fields(json_object)

        for key in properties.keys():
            property_value = properties[key].fget(json_object)

            if key:
                result[key] = _JsonSerialization.get_normalized_value(property_value)

        return result


class Deserializer(object):
    """
    Provides function to deserialize a :class:`JsonObject` from:

    * an `str`
    * a file-like object
    * a `dict`
    """
    @classmethod
    def from_json_string(cls, json_string, target=None):
        """
        Deserialize a string into a :class:`JsonObject`.

        :param json_string: The `str` from which the `JsonObject` should be deserialized.
        :param target: The target `JsonObject` type into which the data from the json string should be deserialized. If
        this is `None` then the object with the most matching fields will be searched.

        :return: The corresponding `JsonObject`.
        :raises ConfigurationError: When the target `JsonObject` doesnt define any fields.
        :raises FieldValidationError: When a field constraint has been violated e.g. a required field is missing.
        :raises TypeError: When the target `JsonObject` didn't have any matching field with the JSON object inside the
        `str`.

        :raises MissingObjectError: When no target `JsonObject` was specified and no matching `JsonObject` could be
        found.
        """
        return cls.from_json_dict(json.loads(json_string), target)

    @classmethod
    def from_json_file(cls, json_file, target=None):
        """
        Deserialize a JSON file into a :class:`JsonObject`.

        :param json_file: A `.read()`-supporting file-like object from which the `JsonObject` should be deserialized.
        :param target: The target `JsonObject` type into which the data from the json string should be deserialized. If
        this is `None` then the object with the most matching fields will be searched.

        :return: The corresponding `JsonObject`.
        :raises ConfigurationError: When the target `JsonObject` doesnt define any fields.
        :raises FieldValidationError: When a field constraint has been violated e.g. a required field is missing.
        :raises TypeError: When the target `JsonObject` didn't have any matching field with the JSON object inside the
        file-like object.

        :raises MissingObjectError: When no target `JsonObject` was specified and no matching `JsonObject` could be
        found.
        """
        return cls.from_json_dict(json.load(json_file), target)

    @classmethod
    def from_json_dict(cls, json_dict, target=None):
        """
        Deserialize a `dict` into a :class:`JsonObject`.

        :param json_dict: A `dict` from which the `JsonObject` should be deserialized.
        :param target: The target `JsonObject` type into which the data from the json string should be deserialized. If
        this is `None` then the object with the most matching fields will be searched.

        :return: The corresponding `JsonObject`.
        :raises ConfigurationError: When the target `JsonObject` doesnt define any fields.
        :raises FieldValidationError: When a field constraint has been violated e.g. a required field is missing.
        :raises TypeError: When the target `JsonObject` didn't have any matching field with the JSON object inside the
        `dict`.

        :raises MissingObjectError: When no target `JsonObject` was specified and no matching `JsonObject` could be
        found.
        """
        if target is None:
            target = _JsonDeserialization.get_most_matching_json_object(json_dict)

        result = target()
        _JsonDeserialization.validate_if_required_fields_satisfied(result, json_dict)

        properties = _JsonCommon.get_decorated_properties(result)
        if not properties:
            raise ConfigurationError("The class doesn't define any fields")
        if all(properties.get(key) is None for key in json_dict.keys()):
            raise TypeError("No matching fields found to build a JsonObject with the type `{}`".format(type(result)))

        for p in properties.keys():
            value = _JsonDeserialization.reverse_normalized_value(json_dict.get(p))
            properties[p].fset(result, value)

        _JsonValidation.validate_fields(result)

        return result


class _JsonCommon(object):
    @classmethod
    def get_decorated_properties(cls, obj):
        """
        Get all properties from an object which are annotated with the `field()` decorator.

        :param obj: The instance of the object from which the properties should be extracted.
        :return: A `dict` containing all properties which are decorated with the `field()` decorator.
        In this `dict` the key is the name of the field (how it should appear in the JSON) and the value is the
        corresponding `property`.
        """
        result = {}

        for member in inspect.getmembers(type(obj)):
            if type(member[1]) == property:
                if "__wrapped__" in member[1].fget.__dict__.keys():
                    member[1].fget(obj)
                    wrapper = member[1].fget.__wrapped__

                    if _JsonField.get_field_name(wrapper):
                        result[_JsonField.get_field_name(wrapper)] = member[1]

        return result

    @classmethod
    def value_is_simple_type(cls, value):
        """
        Check if a property has a simple type which can be simply serialized without any further work.

        :param value: The value which should be checked.
        :return: `True` if the values type is simple; `False` otherwise.
        """
        return (
            type(value) is str or
            type(value) is int or
            type(value) is float
        )

    @classmethod
    def value_not_str_and_iterable(cls, value):
        """
        Check if a property of a class is iterable and **NOT** a `str`.

        :param value: The value which should be checked.
        :return: `True` if the value is iterable and **NOT** a `str`; `False` otherwise.
        """
        return type(value) is not str and isinstance(value, collections.Iterable)


class _JsonSerialization(object):
    @classmethod
    def get_normalized_value(cls, value):
        """
        Check if a value is JSON serializable and if necessary normalize/transform it so that it can be serialized.

        :param value: The value which should be checked and possibly normalized/transformed.
        :raises TypeError: When the type of the value is not JSON serializable.
        :return: The normalized value which can be serialized.
        """
        if value is None:
            return value
        elif _JsonCommon.value_is_simple_type(value):
            return value
        elif isinstance(value, dict):
            result = {}
            for key in value.keys():
                result[key] = cls.get_normalized_value(value[key])

            return result
        elif _JsonCommon.value_not_str_and_iterable(value):
            result = []
            for item in value:
                result.append(cls.get_normalized_value(item))

            return result
        elif isinstance(value, JsonObject):
            return Serializer.to_json_dict(value)
        elif isinstance(value, datetime.datetime):
            if value.tzinfo:
                return value.strftime(DATETIME_TZ_FORMAT)
            else:
                return value.strftime(DATETIME_FORMAT)
        elif isinstance(value, datetime.date):
            return value.strftime(DATE_FORMAT)
        else:
            raise TypeError("The object type `{}` is not JSON serializable".format(type(value)))


class _JsonDeserialization(object):
    @classmethod
    def reverse_normalized_value(cls, normalized_value):
        """
        Reverse the normalization of a value e.g. from a date string like '2018-08-09' create a :class:`datetime.date`
        or for a given `dict` search the appropriate :class:`JsonObject` and return the object with values from the
        `dict`. See also `get_normalized_value()`

        :param normalized_value: The value of which the normalization should be reversed.
        :raises TypeError: When the normalization of the value cannot be reversed.
        :raises ValueError: When a passed value did not match the expectations e.g. datetime.date day was 90
        :return: The reversed value of the normalized field.
        """
        if normalized_value is None:
            return normalized_value
        elif _JsonCommon.value_is_simple_type(normalized_value):
            if type(normalized_value) is str:
                if re.match(_DATE_FORMAT_REGEX, normalized_value):
                    return datetime.datetime.strptime(normalized_value, DATE_FORMAT).date()
                elif re.match(_DATETIME_FORMAT_REGEX, normalized_value):
                    return datetime.datetime.strptime(normalized_value, DATETIME_FORMAT)
                elif re.match(_DATETIME_TZ_FORMAT_REGEX, normalized_value):
                    return parser.isoparse(normalized_value)

            return normalized_value
        elif isinstance(normalized_value, dict):
            try:
                return Deserializer.from_json_dict(normalized_value)
            except MissingObjectError:
                pass

            return {key: cls.reverse_normalized_value(normalized_value[key]) for key in normalized_value.keys()}
        elif type(normalized_value) is list:
            result = []
            for item in normalized_value:
                result.append(cls.reverse_normalized_value(item))

            return result
        else:
            raise TypeError("The normalization for the object type `{}` cannot be reversed"
                            .format(type(normalized_value)))

    @classmethod
    def get_most_matching_json_object(cls, value):
        """
        Given a `dict` check which :class:`JsonObject` matches it the most.

        :param value: The `dict` for which the :class:`JsonObject` should be searched.
        :return: The :class:`JsonObject` which matched mostly with the given `dict`; `None` if none of the objects did
        match.
        """
        key_occurrences = "occurrences"
        key_object = "object"
        matching_objects = []

        for json_object in JsonObject.__subclasses__():
            occurrences = 0
            properties = _JsonCommon.get_decorated_properties(json_object())

            for value_property in value.keys():
                for object_property in properties.keys():
                    if value_property == object_property:
                        occurrences += 1
                        break

            if occurrences:
                matching_objects.append({
                    key_occurrences: occurrences,
                    key_object: json_object
                })

        if matching_objects:
            return sorted(matching_objects, key=lambda x: x[key_occurrences], reverse=True)[0][key_object]

        raise MissingObjectError("No matching JsonObject could be found")

    @classmethod
    def validate_if_required_fields_satisfied(cls, json_object, json_dict):
        """
        Check if all required fields of a :class:`JsonObject` are satisfied.

        :param json_object: The JsonObject which should be checked.
        :raises FieldValidationError: When a required field is missing.
        """
        required_field_names = []
        properties = _JsonCommon.get_decorated_properties(json_object)
        for key in properties.keys():
            if _JsonField.get_required(properties[key].fget):
                required_field_names.append(key)

        for field_name in required_field_names:
            if field_name not in json_dict.keys():
                raise FieldValidationError("The field `{}` is missing".format(field_name))


class _JsonField(object):
    @classmethod
    def get_field_name(cls, property_getter):
        """
        Get the Value of the _JSON_FIELD_NAME attribute of a property getter function.

        NOTE
        ====
        If the property getter is annotated with multiple decorators it will search all wrappers.

        :param property_getter: The function which should be checked for the _JSON_FIELD_NAME attribute.
        :return: The name of the field if it could be found; `None` otherwise.
        """
        return cls._get_field_attribute(property_getter, _JSON_FIELD_NAME)

    @classmethod
    def get_required(cls, property_getter):
        """
        Get the value of the _JSON_FIELD_REQUIRED attribute of a property getter function.

        NOTE
        ====
        If the property getter is annotated with multiple decorators it will search all wrappers.

        :param property_getter: The function which should be checked for the _JSON_FIELD_REQUIRED attribute.
        :return: `True` if the field is required: `False` otherwise.
        """
        return cls._get_field_attribute(property_getter, _JSON_FIELD_REQUIRED) or False

    @classmethod
    def get_nullable(cls, property_getter):
        """
        Get the value of the _JSON_FIELD_NULLABLE attribute of a property getter function.

        NOTE
        ====
        If the property getter is annotated wit multiple decorators it will search all wrappers.

        :param property_getter: The function which should be checked for the _JSON_FIELD_NULLABLE attribute.
        :return: `True` if the field is nullable; `False` otherwise.
        """
        return cls._get_field_attribute(property_getter, _JSON_FIELD_NULLABLE) or False

    @classmethod
    def _get_field_attribute(cls, func, attr_name):
        if hasattr(func, attr_name):
            return getattr(func, attr_name)

        if "__wrapped__" in func.__dict__.keys():
            return cls._get_field_attribute(func.__wrapped__, attr_name)

        return None


class _JsonValidation(object):
    @classmethod
    def validate_fields(cls, json_object):
        """
        Validate the fields of a :class:`JsonObject`.

        :param json_object: The `JsonObject` which should be validted.
        :raises FieldValidationError: When a field violated it's constraints.
        """
        properties = _JsonCommon.get_decorated_properties(json_object)
        cls._validate_not_nullable_fields(json_object, properties)

    @classmethod
    def _validate_not_nullable_fields(cls, json_object, properties):
        """
        Validate if all fields of a :class:`JsonObject` which are **NOT** nullable are **NOT** null.

        :param json_object: The `JsonObject` which should be checked.
        :param properties: The properties of the passed `JsonObject` which are decorated with the `field` decorator as
        a dict of the field name and the property.
        :raises FieldValidationError: When a property was null even though it wasn't allowed to.
        """
        for key in properties:
            if not _JsonField.get_nullable(properties[key].fget):
                value = properties[key].fget(json_object)
                cls._check_for_null_values(key, value)

    @classmethod
    def _check_for_null_values(cls, field_name, value):
        if value is None:
            raise FieldValidationError("The field `{}` is not allowed to be None".format(field_name))
        elif isinstance(value, dict):
            for k, v in value.items():
                cls._check_for_null_values(field_name, v)
        elif _JsonCommon.value_not_str_and_iterable(value):
            for item in value:
                cls._check_for_null_values(field_name, item)
        elif isinstance(value, JsonObject):
            properties = _JsonCommon.get_decorated_properties(value)
            cls._validate_not_nullable_fields(value, properties)

