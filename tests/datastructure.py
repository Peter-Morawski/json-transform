# -*- coding: utf-8 -*-

from decorator import decorator

from jsontransform import FieldMode, JSONObject, field


@decorator
def some_decorator(func, *args, **kwargs):
    if not hasattr(func, "_was_wrapped_with_some_decorator"):
        func._was_wrapped_with_some_decorator = True

    return func(*args, **kwargs)


class Container(JSONObject):
    CONTAINER_FIELD_NAME = "container"

    def __init__(self):
        super(Container, self).__init__()
        self._container = None

    @property
    @field(CONTAINER_FIELD_NAME)
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


class JSONObjectWithoutFields(JSONObject):
    def __init__(self):
        super(JSONObjectWithoutFields, self).__init__()
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


class Car(JSONObject):
    FIELD_MODEL_NAME_NAME = "modelName"
    FIELD_MAX_SPEED_NAME = "maxSpeed"

    def __init__(self):
        super(Car, self).__init__()
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


class ExtendedExtendedCar(ExtendedCar):
    FIELD_COLOR_NAME = "color"

    def __init__(self):
        super(ExtendedExtendedCar, self).__init__()
        self._color = ""

    @property
    @field()
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value


class JSONObjectWithRequiredField(JSONObject):
    SOME_FIELD_NAME = "someField"
    REQUIRED_FIELD_NAME = "requiredField"

    def __init__(self):
        super(JSONObjectWithRequiredField, self).__init__()
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


class IssueType(JSONObject):
    ID_NAME = "id"
    DESCRIPTION_NAME = "description"
    ICON_URL = "iconUrl"
    NAME_NAME = "name"
    SUB_TASK_NAME = "subTask"

    def __init__(self):
        super(IssueType, self).__init__()
        self._id = u""
        self._description = u""
        self._icon_url = u""
        self._name = u""
        self._sub_task = False

    @property
    @field(ID_NAME, required=True)
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    @field(DESCRIPTION_NAME, required=True)
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    @field(ICON_URL, required=True)
    def icon_url(self):
        return self._icon_url

    @icon_url.setter
    def icon_url(self, value):
        self._icon_url = value

    @property
    @field(NAME_NAME, required=True)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    @field(SUB_TASK_NAME, required=True)
    def sub_task(self):
        return self._sub_task

    @sub_task.setter
    def sub_task(self, value):
        self._sub_task = value


class IssuePriority(JSONObject):
    ID_NAME = "name"
    ICON_URL_NAME = "iconUrl"
    NAME_NAME = "name"

    def __init__(self):
        super(IssuePriority, self).__init__()
        self._id = u""
        self._icon_url = u""
        self._name = u""

    @property
    @field(ID_NAME, required=True)
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    @field(ICON_URL_NAME, required=True)
    def icon_url(self):
        return self._icon_url

    @icon_url.setter
    def icon_url(self, value):
        self._icon_url = value

    @property
    @field(NAME_NAME, required=True)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class ContainerWithFieldModeEncodeOnly(JSONObject):
    ENCODE_ONLY_NAME = "encodeOnly"

    def __init__(self):
        super(ContainerWithFieldModeEncodeOnly, self).__init__()
        self._encode_only = None

    @property
    @field(ENCODE_ONLY_NAME, required=True, mode=FieldMode.ENCODE)
    def encode_only(self):
        return self._encode_only

    @encode_only.setter
    def encode_only(self, value):
        self._encode_only = value


class ContainerWithFieldModeDecodeOnly(JSONObject):
    DECODE_ONLY_NAME = "decodeOnly"

    def __init__(self):
        super(ContainerWithFieldModeDecodeOnly, self).__init__()
        self._decode_only = None

    @property
    @field(DECODE_ONLY_NAME, required=True, mode=FieldMode.DECODE)
    def decode_only(self):
        return self._decode_only

    @decode_only.setter
    def decode_only(self, value):
        self._decode_only = value
