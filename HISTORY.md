# History

## 0.2.0 (2018-08-27)

* added support for the type unicode

## 0.1.9.1 (2018-08-23)

* fixed the problem where the type bool would not be recognized during serialization/deserialization

## 0.1.9 (2018-08-21)

* removed the serialization and deserialization logic from the JsonObject and created separate objects for serializing and
deserializing

## 0.1.8 (2018-08-19)

* added the **nullable** parameter to the `field()` decorator which indicates that a field is nullable during
serialization and deserialization

## 0.1.7 (2018-08-16)

* added the **required** parameter to the `field()` decorator which indicates that a field is required during the
deserialization
* fixed the deserialization of a dict which doesnt have an appropriate JsonObject so that all it's values are reversed
from the normalization process

## 0.1.6 (2018-08-15)

* fixed the deserialization of JSON objects inside a list/iterable
* fixed regex for datetimes that have a timezone with negative utc offset 

## 0.1.5.1 (2018-08-11)

* packaging fix after changing the name of the repo

## 0.1.5 (2018-08-08)

* first release of the package
* possibility to serialize and deserialize python objects by inheriting from **JsonObject** and annotating property
getters with the `field()` decorator
* add custom name to fields by passing a string into the `field()` decorator
