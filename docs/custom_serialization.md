# Custom Serialization and Deserialization Guide

This guide shows you how to extend `rds2py` to support custom Python classes. By implementing custom readers and writers, you can serialize your custom Python representations directly into native R RDS/RData structures, and read them back seamlessly.

`rds2py` achieves this two-way extensibility using:
1. Python's `functools.singledispatch` mechanism for writing/serialization (`save_rds`).
2. A global class mapping registry for reading/deserialization (`read_rds`).

---

## 1. Custom Serialization (Python -> RDS)

To serialize a custom Python class, you register it with the `save_rds` generic dispatcher. Your custom function needs to take your object and convert it into a structured dictionary that matches R's internal representation format.

### The Structured RDS Representation Format
R objects are represented in Python as nested dictionaries containing the following keys:
- `"type"`: The R type descriptor (e.g., `"S4"`, `"vector"`, `"integer"`, `"double"`, `"string"`, `"logical"`, or `"null"`).
- `"class_name"`: The target R class name (e.g., `"MyCustomRClass"`).
- `"package_name"`: *(Optional, for S4 classes)* The name of the R package where the class is defined.
- `"attributes"`: A dictionary representing R attributes or S4 slots. Each slot value must also be a structured representation dictionary.
- `"data"`: The flat list or array of values for vector/atomic types.

### Example: Implementing a Custom Serializer

Let's say we have a custom Python class named `MyFeature`:

```python
class MyFeature:
    def __init__(self, name: str, values: list):
        self.name = name
        self.values = values
```

To serialize `MyFeature` as a native R S4 class called `"MyCustomRClass"` from package `"MyRPackage"`, we register it using `@save_rds.register`:

```python
from typing import Optional
from rds2py import save_rds


@save_rds.register(MyFeature)
def _save_rds_myfeature(x: MyFeature, path: Optional[str] = None):
    # Native C++ writer call
    from rds2py.lib_rds_parser import write_rds as write_rds_native

    # 1. Structure the Python object into the expected R dictionary format
    converted = {
        "type": "S4",
        "class_name": "MyCustomRClass",
        "package_name": "MyRPackage",
        "attributes": {
            # Recursively call save_rds to serialize internal elements
            "featureName": save_rds(x.name),
            "featureValues": save_rds(x.values),
        },
    }

    # 2. If a save path is specified, write directly using the native writer
    if path is not None:
        write_rds_native(converted, path)

    return converted
```

---

## 2. Custom Deserialization (RDS -> Python)

To read custom S4 objects back into Python classes via `read_rds`, you need to:
1. Write a deserialization function that constructs your Python class from the raw parsed dictionary.
2. Register your deserializer function in `rds2py`'s global class mapping registry.

### Example: Implementing the Reader

```python
from rds2py.generics import _dispatcher
from rds2py.rdsutils import get_class


def read_my_custom_class(robject: dict, **kwargs) -> MyFeature:
    # 1. Verify the incoming R class name
    cls_name = get_class(robject)
    if cls_name != "MyCustomRClass":
        raise ValueError(f"Expected class 'MyCustomRClass', but received '{cls_name}'")

    # 2. Extract and parse the slots recursively
    # We call the internal _dispatcher helper to parse child structures
    feature_name = _dispatcher(robject["attributes"]["featureName"], **kwargs)
    feature_values = _dispatcher(robject["attributes"]["featureValues"], **kwargs)

    # 3. Instantiate and return your custom Python class
    return MyFeature(name=feature_name, values=list(feature_values))
```

### Registering the Reader
Map your class name to the reader function in the global class registry (`REGISTRY` from `rds2py.generics`):

```python
from rds2py.generics import REGISTRY

# Register our custom deserializer in the global map
REGISTRY["MyCustomRClass"] = read_my_custom_class
```

---

## 3. Full Roundtrip

Here is how the entire custom serialization and deserialization workflow works together:

```python
import tempfile
import os
from rds2py import write_rds, read_rds

# 1. Create a custom instance
feature = MyFeature(name="expression_level", values=[10, 20, 30])

# 2. Serialize to a temporary RDS file
with tempfile.NamedTemporaryFile(suffix=".rds", delete=False) as tmp:
    path = tmp.name

try:
    # Write custom class to RDS format
    write_rds(feature, path)

    # Read the RDS file back into Python
    recreated = read_rds(path)

    # 3. Verify that the roundtrip correctly recreated the custom class
    assert isinstance(recreated, MyFeature)
    assert recreated.name == "expression_level"
    assert recreated.values == [10, 20, 30]
    print("Roundtrip validation successful!")
finally:
    if os.path.exists(path):
        os.unlink(path)
```
