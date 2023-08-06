# Mooss - Serialize

**⚠️ This package is a work-in-progress, it is not suitable nor reliable for any applications yet ⚠️**

A Python package to help with serialization and deserialization of *dataclasses* through the help of a common interface
while also insuring the parsed data is properly typed and handled in many situations.

This package was created because I often found myself needing to deserialize nested dataclasses with *complex* value
types, and because all other solutions I found were either too bloated or didn't work properly with what I had.<br>
It is by no mean a replacement for other packages, but [...].

[strong typecheck, with actual recursive typecasting]

[Intended to parse data from text, no strong security against lambdas, callables !!!]

## Setup

### Requirements
* Python 3.9 or newer.

### Installation
Run one of the following commands to install the package:
```bash
python -m pip install --upgrade mooss-serialize
pip install --upgrade mooss-serialize
```

## Usage
In order to use this package, you simply have to create a class that extends the provided `ISerializable` interface
that also has the `dataclass` decorator, add some variable annotations with the desired types, and then use the
provided class methods to serialize and deserialize it easily.

See the examples below for more information

### Creating classes
The following classes have more complex and fluid typing for their variables that will help illustrate the main
advantage of this package over oneliners and other simpler deserializers.
```python
from dataclasses import dataclass
from typing import Optional, Union

from mooss.serialize.interface import ISerializable

@dataclass
class Address(ISerializable):
    country: str
    city: str
    zip_code: Optional[int]
    # TODO: non-serializable bool
    street: str = "Unknown"

@dataclass
class Person(ISerializable):
    name: str
    address: Union[Address, str, None]
```

### Preparing the raw data
[Can be from json, toml or raw as a dict]
```python
# All of the fields with nested 'ISerializable' classes
data_person_full: dict = {
    "name": "John Smith",
    "address": {
        "country": "Belgium",
        "city": "Brussels",
        "zip_code": 1000,
        "street": "Rue de la Tribune",
    },
}
```

### Parsing the data
```python
person_full = Person.from_dict(data_person_full)

print(person_full)
```

## Type annotations
Since the `dataclass` decorator is required on any class that extends `ISerializable`, the methods can easily detect
and validate the different types for the given data, which in turn can help you reduce the amount of check you will
have to perform on the final deserialized data.

This approach was used due to the fact that many one-liners and small helpers available on the internet do not
implement this type of checks and usually leave you with potentially invalidly-typed data, or simply data that is not
deserialized properly in the case of nested deserializable classes.

// Any other object type should be ignored and if possible, instantiated as a dict.

### Supported types
These types should cover 99% of the uses cases for this package, however, in the event you would wish to use
unsupported types, you can always do so by [... auto_typecast ?]

* **Primitives:**<br>
`str`, `int`, `float`, `bool`
* **Simple sets:**<br>
`list`, `dict`, `tuple`, `set`
* **Composed sets\*:**<br>
`list[...]`, `dict[...]`, `tuple[...]`, `set[...]`
* **Variable types\*:**<br>
`Union`, `Optional`, `Any`

<sup>*: Has some limitations on what can be contained between the square brackets.</sup>

### Limitations
These limitations are put in place due to the fact that I don't have the time to implement a proper way to
support weird and unusual data types.

[...] If you want to handle these, you can either add support for it yourself or use a specialized and bulkier
package.

* Mixed complex types: list[ISerializable, primitive]
  * A mix of primitives and sets should work but should preferably not be used.

#### More specific and rare types
Types and utilities such as the ones listed below should be supported at some point, but since it is not urgent,
there is no set timeline for their implementation.

*List of types and utilities that may be supported:*<br>
`Set`, `Collection`, `NamedTuple`, `NewType`, `Mapping`, `Sequence`, `TypeVar` and `Iterable`.

## Contributing
If you want more information on how to contribute to this package, you should refer to [develop.md](develop.md).

## License
[Unlicense](LICENSE)
