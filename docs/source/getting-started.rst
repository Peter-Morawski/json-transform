.. _getting-started:

.. module:: jsontransform

Getting Started
===============

This guide will show you how you can start using json-transform in order to simplify your JSON object parsing.

What you'll learn
-----------------

You'll learn how to define a JSON object in python using json-transform and how to encode your object instance into
a JSON file as well as deserialize it from one.

Installing json-transform
-------------------------

Before you can start testing the following examples, you first need to install json-transform. To do this simply visit the
:ref:`Installation <installation>` Page and follow the PyPI guide there.

Defining our first JSONObject using json-transform
---------------------------------------------------

Now that you have successfully installed json-transform we can finally start defining your first :py:class:`JSONObject`.
To do that you have to create a Plain Old Python Object. It can have any amount of methods, properties, etc...
The important part is

1. it needs to extend the :py:class:`JSONObject` class so that json-transform will recognize that this object is
intended to be a encodable and decodable to a JSON document.

2. it needs to have at least one property decorated with the :py:func:`field` decorator.

So let's define a simple entity.

.. code-block:: python

    from jsontransform import JSONObject, field


    class Person(JSONObject):
        def __init__(self):
            self._first_name = ""
            self._last_name = ""

        @property
        @field("firstName", required=True)
        def first_name(self):
            return self._first_name

        @first_name.setter
        def first_name(self, value):
            self._first_name = value

        @property
        @field("lastName")
        def last_name(self):
            return self._last_name

        @last_name.setter
        def last_name(self, value):
            self._last_name = value


In this example we have given the `first_name` and the `last_name` property a custom **field_name** so when we encode
our :py:class:`JSONObject` the fields in the resulting JSON document will be called **firstName** and **lastName**. The
same applies for the decoding. The decoder will search for fields called *firstName* and *lastName*. We will see this
later in action.


Besides a **field_name** the `first_name` property has the **required** parameter set to True. This means that this
:py:func:`field` is mandatory when we want to decode a JSON document into our :py:class:`JSONObject`.


Now that we have defined our entity let's create an instance of it.

.. code-block:: python

    peter = Person()
    peter.first_name = "Peter"
    peter.last_name = "Parker"

Encoding
--------

When we want to encode our :py:class:`JSONObject` we can use the following functions

- :py:func:`dump` to encode it into a `write()` supporting file-like object
- :py:func:`dumps` to encode it into an `str` or
- :py:func:`dumpd` to encode it into a `dict`

It is also possible to encode our :py:class:`JSONObject` using the :py:class:`JSONEncoder` but to keep it simple we will
use the :py:func:`dumpd` function to encode our :py:class:`JSONObject` into a `dict`.


To keep things simple we will use the :py:func:`dumpd` function to encode our :py:class:`JSONObject` into a dict which
is JSON conform.

.. code-block:: python

    from jsontransform import dumpd

    dumpd(peter)
    # result: {'age': 56, 'birthday': '1962-09-23', 'firstName': 'Peter', 'lastName': 'Parker'}


Decoding
--------

When we want to decode a file, `dict` or an `str` into our :py:class:`JSONObject` we can use the following functions

- :py:func:`load` to decode a :py:class:`JSONObject` from a `read()` supporting file-like object
- :py:func:`loads` to decode a :py:class:`JSONObject` from an `str` or
- :py:func:`loadd` to decode a :py:class:`JSONObject` from a `dict`

We also have a :py:class:`JSONDecoder` which can be instantiated and provides the same functionality like the previously
mentioned functions but to keep it simple we'll use the :py:func:`loadd` function to decode a `dict` into our
:py:class:`JSONObject`.


.. code-block:: python

    from jsontransform import loadd

    peter = loadd({'age': 56, 'birthday': '1962-09-23', 'firstName': 'Peter', 'lastName': 'Parker'})

    print(type(peter))
    # result <class 'Person'>

    print(peter.first_name)
    # result: Peter

    print(peter.last_name)
    # result: Parker

.. note::

    When decoding into a :py:class:`JSONObject` we can specify the target type / the :py:class:`JSONObject` into which
    the JSON document should be decoded OR we can let json-transform find the most matching :py:class:`JSONObject` by
    itself *(like in the example above)*.

After the decoding our fields/properties will be casted into their appropriate type. To see which types
are supported check the :ref:`Fields <fields>` page.
