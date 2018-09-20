# History

## 1.0.1 (2018-09-15)

* fix the installation problem

## 1.0.0 (2018-09-14)

* implement the new/stable API design

## 0.4.1 (2018-09-10)

* fixed wrong object match when searching for the most matching `JSONObject` while deserializing and there were multiple
objects that had the same number of matching occurrences - then the `JSONObject` with the exact same amount of
fields as the `dict` should be taken

## 0.4.0 (2018-09-08)

* added the name of the object to the `FieldValidationError` which is thrown in the `validate_if_required_fields_satisfied`
* fixed the wrong object type when searching the most matching `JSONObject` while deserializing

## 0.3.1 (2018-09-03)

* fix the installation error which was caused in version 0.3.0

## 0.3.0 (2018-09-02)

* added a better compliance for the ISO-8601 date format with a few exceptions which are **NOT** implemented:
  * calendar dates with `YYYY-MM` and `--MM-DD`/`--MMDD`
  * week dates **completely**
  * ordinal dates **completely**

## 0.2.0 (2018-08-27)

* added support for the type unicode

## 0.1.9.1 (2018-08-23)

* fixed the problem where the type bool would not be recognized during serialization/deserialization

## 0.1.9 (2018-08-21)

* removed the serialization and deserialization logic from the JSONObject and created separate objects for serializing and
deserializing

## 0.1.8 (2018-08-19)

* added the **nullable** parameter to the `field()` decorator which indicates that a field is nullable during
serialization and deserialization

## 0.1.7 (2018-08-16)

* added the **required** parameter to the `field()` decorator which indicates that a field is required during the
deserialization
* fixed the deserialization of a dict which doesnt have an appropriate JSONObject so that all it's values are reversed
from the normalization process

## 0.1.6 (2018-08-15)

* fixed the deserialization of JSON objects inside a list/iterable
* fixed regex for datetimes that have a timezone with negative utc offset 

## 0.1.5.1 (2018-08-11)

* packaging fix after changing the name of the repo

## 0.1.5 (2018-08-08)

* first release of the package
* possibility to serialize and deserialize python objects by inheriting from **JSONObject** and annotating property
getters with the `field()` decorator
* add custom name to fields by passing a string into the `field()` decorator
