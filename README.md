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

class DatasetConfig(Struct):
    paths = Array(str, description="Dataset paths.")
    batch_size = Variable(int, description="Batch size", default=64)
    shuffle = Variable(bool, description="Shuffle dataset on the fly", default=True)

class TrainerConfig(Struct):
    learning_rate = Variable(float, description="Learning rate for training", default=0.001)
    epochs = Variable(int, description="Number of training epochs", optional=True)
    training_dataset = DatasetConfig(description="Training datasets")

config = TrainerConfig()
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
print(config.learning_rate)
print(config.training_dataset.batch_size)

# Modifying fields
config.learning_rate = 0.01
config.training_dataset.batch_size = 128

# Using set and get methods
config.set({'learning_rate': 0.01, 'training_dataset': {'paths': '/path/to/data'], 'batch_size': 128}})
print(config.get())
```

### Using the CLI Parser

The CLI parser allows you to override configuration values using command-line arguments. It also supports loading configurations from a file specified via CLI.

```python
from safeconfig import CLIParser

if __name__ == "__main__":
    parser = CLIParser(TrainerConfig())
    config = parser.parse_args()
    print(config)
```

Now you can load configuration files by passing a config file path or override fields with corresponding command line arguments:

```bash
python your_script.py --config path/to/config.yaml \
--learning_rate 0.01 \
--training_dataset.paths /data/dataset1 /data/dataset2
--training_dataset.batch_size 128 \
--print_config
```

Help command will is automatically generated based on the schema:

```bash
python your_script.py --help
```

### Example Configuration

Here is an example configuration file in YAML format:

```yaml
learning_rate: 0.01
epochs: 10
training_dataset:
  paths:
    - "/data/dataset1"
    - "/data/dataset2"
  batch_size: 128
  shuffle: true
```

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
