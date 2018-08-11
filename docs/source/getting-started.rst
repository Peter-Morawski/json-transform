.. _getting-started:

Getting Started
===============

This guide will show you how you can start using json-transform in order to simplify your JSON object parsing.

What you'll learn
-----------------

You'll learn how to define a JSON object in python using json-transform and how to serialize your object instance into:

- a python dict
- a JSON string or
- a JSON file

as well as deserialize it from these.

Installing json-transform
-------------------------

Before you can start testing the following examples, you first need to install json-transform. To do this simply visit the
:ref:`Installation <installation>` Page and follow the appropriate guide there.

Defining our first JSON object in python using json-transform
-------------------------------------------------------------

Now that you have successfully installed json-transform you can finally start defining your first JSON object. To do
that you have to create a POPO (Plain Old Python Object). It can have any amount of methods, properties, etc...
The important part is

1. it needs to extend the :py:class:`JsonObject` class which has the core functions that allow you to serialize and
deserialize your object.
2. it needs to have at least one property getter decorated with the :py:func:`field` decorator.

So let's define a simple data structure.

.. code-block:: python

    from jsontransform import JsonObject, field


    class Person(JsonObject):
        def __init__(self):
            self._first_name = ""
            self._last_name = ""
            self._birthday = None
            self._age = 0

        @property
        @field("firstName")
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

        @property
        @field()
        def birthday(self):
            return self._birthday

        @birthday.setter
        def birthday(self, value):
            self._birthday = value

        @property
        @field()
        def age(self):
            return self._age

        @age.setter
        def age(self, value):
            self._age = value

In this example some of the fields have a custom name defined. For example the first_name which will be called
**"firstName"** in the resulting JSON object.

Now that we have defined our object let's create an instance of it.

.. code-block:: python

    import datetime

    peter = Person()
    peter.first_name = "Peter"
    peter.last_name = "Parker"
    peter.birthday = datetime.date(1962, 9, 23)
    peter.age = 56

Serializing
-----------

We have three different methods to serialize our object:

- :py:func:`to_json_dict`
- :py:func:`to_json_string`
- :py:func:`to_json_file`


to_json_dict
++++++++++++

The :py:func:`to_json_dict` function serializes the instance of an object into a python ``dict``.
Let's try it with our previously created object.

.. code-block:: python

    peter.to_json_dict()
    # result: {'age': 56, 'birthday': '1962-09-23', 'firstName': 'Peter', 'lastName': 'Parker'}

to_json_string
++++++++++++++

The :py:func:`to_json_string` function serializes the instance of an object into a JSON object and returns it as an ``str``.
With our previously created object it will look like follows.

.. code-block:: python

    peter.to_json_string()
    # result: {"age": 56, "birthday": "1962-09-23", "firstName": "Peter", "lastName": "Parker"}

to_json_file
++++++++++++

The :py:func:`to_json_file` function serializes the instance of an object as a JSON object into a file.

.. code-block:: python

    with open("peter.json", "w") as f:
        peter.to_json_file(f)
        # file will contain: {"age": 56, "birthday": "1962-09-23", "firstName": "Peter", "lastName": "Parker"}

Deserializing
-------------

from_json_dict
++++++++++++++

The :py:func:`from_json_dict` function deserializes a python ``dict`` into the target object instance.
Which will look like the following with our :py:class:`Person` object.

.. code-block:: python

    peter = Person.from_json_dict({'age': 56, 'birthday': '1962-09-23', 'firstName': 'Peter', 'lastName': 'Parker'})
    print(peter.first_name)
    # result: Peter

    print(peter.last_name)
    # result: Parker

    print(peter.birthday)
    # result: 1962-09-23

    print(peter.age)
    # result: 56

After the deserialization most of our fields/properties will be casted into their appropriate type. To see which types
are supported check the :ref:`Fields <fields>` page.

Here are some examples:

.. code-block:: python

    print(type(peter.first_name))
    # result: <class 'str'>

    print(type(peter.last_name))
    # result: <class 'str'>

    print(type(peter.birthday))
    # result: <class 'datetime.date'>

    print(type(peter.age))
    # result: <class 'int'>

from_json_string
++++++++++++++++

The :py:func:`from_json_string` function deserializes an ``str`` which contains a JSON object inside into the target
object instance. Let's try it with our object.

.. code-block:: python

    peter = Person.from_json_string("{'age': 56, 'birthday': '1962-09-23', 'firstName': 'Peter', 'lastName': 'Parker'}")
    print(peter.first_name)
    # result: Peter

    print(peter.last_name)
    # result: Parker

    print(peter.birthday)
    # result: 1962-09-23

    print(peter.age)
    # result: 56

from_json_file
++++++++++++++

The :py:func:`from_json_file` function creates an instance of our target object from a file which contains a JSON object.
So let's try it.

.. code-block:: python

    with open("peter.json", "r") as f:
        peter = Person.from_json_file(f)
        print(peter.first_name)
        # result: Peter

        print(peter.last_name)
        # result: Parker

        print(peter.birthday)
        # result: 1962-09-23

        print(peter.age)
        # result: 56
