# -*- coding: utf-8 -*-

from jsontransform import JsonObject, field
from decorator import decorator


@decorator
def some_decorator(func, *args, **kwargs):
    if not hasattr(func, "_was_wrapped_with_some_decorator"):
        func._was_wrapped_with_some_decorator = True

    return func(*args, **kwargs)


class Container(JsonObject):
    CONTAINER_FIELD_NAME = "container"

    def __init__(self):
        self._container = None

    @property
    @field()
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        self._container = value


class ContainerWithSomeDecoratorBeforeField(Container):
    @property
    @some_decorator
    @field()
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        self._container = value


class ContainerWithSomeDecoratorAfterField(Container):
    @property
    @field()
    @some_decorator
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        self._container = value


class JsonObjectWithoutFields(JsonObject):
    def __init__(self):
        self._something = 0

    @property
    def something(self):
        return self._something

    @something.setter
    def something(self, value):
        self._something = value


class NotSerializableObject(object):
    def __init__(self):
        self._name = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


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


class JsonObjectWithRequiredField(JsonObject):
    SOME_FIELD_NAME = "someField"
    REQUIRED_FIELD_NAME = "requiredField"

    def __init__(self):
        self._some_field = None
        self._required_field = None

    @property
    @field(SOME_FIELD_NAME)
    def some_field(self):
        return self._some_field

    @some_field.setter
    def some_field(self, value):
        self._some_field = value

    @property
    @field(REQUIRED_FIELD_NAME, required=True)
    def required_field(self):
        return self._required_field

    @required_field.setter
    def required_field(self, value):
        self._required_field = value
