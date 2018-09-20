# JSON-Transform

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a1aab0fd1e964a729749f6d2c962551c)](https://www.codacy.com/app/pmorawski/json-transform?utm_source=Peter-Morawski@bitbucket.org&amp;utm_medium=referral&amp;utm_content=Peter-Morawski/json-transform&amp;utm_campaign=Badge_Grade)

JSON-Transform allows you to simply convert your Python objects into a JSON document and vice versa.

New? Here is some help:

* [Getting Started](https://json-transform.readthedocs.io/en/latest/getting-started.html#getting-started)

### Example

Setup your object/entity.

```python
from jsontransform import field, JSONObject


class Customer(JSONObject):
    def __init__(self):
        self._first_name = ""
    
    # set a custom name for the field because by default it will be the function name
    @property
    @field("firstName")
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        self._first_name = value
```

Instantiate the object and encode it to a JSON document.

```python
from jsontransform import dumpd, dump, dumps

new_customer = Customer()
new_customer.first_name = "Peter"

# get a dict representation of the object
dumpd(new_customer)
# result: {"firstName": "Peter"}

# get an str with with our encoded object
dumps(new_customer)
# result: '{"firstName": "Peter"}'

# we can also encode the object directly into a file
with open("new_customer.json", "w") as f:
    dump(new_customer, f)
```


**JSON file (new_customer.json):**

```json
{
  "firstName": "Peter"
}
```

Decode a JSON document.

**Code:**

```python
from jsontransform import load, loadd, loads

# we can decode our customer object from a JSON file
with open("new_customer.json", "r") as f:
    customer = load(f)
    
# or a dict
customer = loadd({"firstName": "Peter"})

# or an str as well
customer = loads("{'firstName': 'Peter'}")

customer.first_name
# result: Peter
```

### More

* Check out the [documentation](https://json-transform.readthedocs.io/en/latest/).
* Check out the [history](https://github.com/Peter-Morawski/json-transform/blob/master/HISTORY.md)
* Check out the [API design](https://github.com/Peter-Morawski/json-transform/wiki/API-Design)
