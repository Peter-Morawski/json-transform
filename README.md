# JSON Transform

Json Transform allows you to simply serialize your Python objects into a JSON format and vice versa.

New? Here is some help:

* [Getting Started](#)

### Example

Setup your object.

```python
from jsontransform import field, JsonObject


class Customer(JsonObject):
    def __init__(self):
        self._first_name = ""
        self._age = 0
    
    # set a custom name for the field becuase by default it will be the function name
    @property
    @field("firstName")
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        self._first_name = value
    
    @property
    @field()
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        self._age = value
```

Instantiate the object and serialize it.

```python
new_customer = Customer()
new_customer.first_name = "Peter"
new_customer.age = 1

# get a dict representation of the object
# result: {"firstName": "Peter", "age": 1}
new_customer.to_json_dict()

# we can also write the object directly into a file
with open("new_customer.json", "w") as f:
    new_customer.to_json_file(f)
```

Deserialize a JSON file into your object.

**JSON file (customer.json):**

```json
{
  "firstName": "Dennis",
  "age": 70
}
```

**Code:**

```python
# we load our customer object
with open("customer.json", "r") as f:
    customer = Customer.from_json_file(f)
    
customer.age
# result: 70

customer.first_name
# result: Dennis
```

### More

Check out the [documentation](#).
