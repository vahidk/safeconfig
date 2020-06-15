# SafeConfig Library

## Overview

SafeConfig provides a structured and flexible way to define, validate, and manage configurations for your Python applications. It supports hierarchical configuration structures with fields that can be variables, arrays, or nested structures. It also includes a command-line interface (CLI) parser to easily override configurations via CLI arguments.

## Features

- Define hierarchical configurations with nested structures.
- Support for variable, array, and struct field types.
- Validation of field values.
- Load and save configurations from/to JSON and YAML files.
- Override configurations using command-line arguments.

## Installation

To install the library, clone the repository and install the required dependencies:

```bash
pip install safeconfig
```

## Usage

### Defining a Configuration

To define a configuration, create a class that inherits from `Struct` and define the fields using `Variable`, `Array`, and other `Struct` subclasses.

```python
from safeconfig import Variable, Array, Struct

class SubConfig(Struct):
    field1 = Variable(int, description="An integer field", default=10)
    field2 = Variable(str, description="A string field", default="default")

class MyConfig(Struct):
    int_var = Variable(int, description="An integer variable", default=1)
    str_var = Variable(str, description="A string variable", default="hello")
    arr_var = Array(int, description="An array of integers", default=[1, 2, 3])
    struct_var = SubConfig(description="A nested struct")

config = MyConfig()
```

### Loading Configuration from a File

You can load the configuration from a JSON or YAML file using the `read` method.

```python
config.read("path/to/config.yaml")
```

Note that the Struct will be used as a schema to validate all the attributes.

### Saving Configuration to a File

You can save the configuration to a JSON or YAML file using the `write` method.

```python
config.write("path/to/config.yaml")
```

### Accessing and Modifying Configuration

You can access and modify the configuration fields directly or using the `set` and `get` methods.

```python
# Accessing fields
print(config.int_var)
print(config.struct_var.field1)

# Modifying fields
config.int_var = 42
config.struct_var.field1 = 20

# Using set and get methods
config.set({'int_var': 42, 'struct_var': {'field1': 20}})
print(config.get())
```

### Using the CLI Parser

The CLI parser allows you to override configuration values using command-line arguments. It also supports loading configurations from a file specified via CLI.

```python
from safeconfig import CLIParser

if __name__ == "__main__":
    parser = CLIParser(MyConfig())
    config = parser.parse_args()
    print(config)
```

Now you can load configuration files by passing a config file path or override fields with corresponding command line arguments:

```bash
python your_script.py --config path/to/config.yaml \
--int_var 42 \
--struct_var.field1 20 \
--print_config
```

Help command will is automatically generated based on the schema:

```bash
python your_script.py --help
```

### Example Configuration

Here is an example configuration file in YAML format:

```yaml
int_var: 5
str_var: "example"
arr_var:
  - 1
  - 2
  - 3
struct_var:
  field1: 100
  field2: "nested value"
```

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
