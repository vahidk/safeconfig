import copy
import json
import os
from typing import Optional

import yaml

from .field import _Field


class Struct(_Field):
    """Class representing a structured field."""

    def __init_subclass__(cls, **kwargs):
        """
        Initialize a subclass of Struct.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init_subclass__(**kwargs)
        schema = {}
        for name, value in cls.__dict__.items():
            if not name.startswith("_"):
                if isinstance(value, _Field):
                    schema[name] = value
                else:
                    raise TypeError(
                        "Attributes must be of type Field. "
                        f"Invalid attribute '{name}' of type {type(value).__name__}."
                    )
        for name in schema.keys():
            delattr(cls, name)
        cls._schema = schema

    def __init__(self, description: Optional[str] = None, optional: bool = False):
        """
        Initialize a structured field.

        Args:
            description (Optional[str]): Description of the struct.
            optional (bool): Whether the struct is optional.
        """
        if self.__class__ == Struct:
            raise TypeError("Struct class cannot be instantiated directly.")

        self._fields = {} if optional else copy.deepcopy(self._schema)
        super().__init__(
            data_type=self.__class__,
            description=description,
            optional=optional,
        )

    def set(self, value: any):
        """
        Set the value of the struct.

        Args:
            value (any): The value to be set.

        Raises:
            AttributeError: If the value is invalid.
        """
        if value is None:
            if not self._optional:
                raise AttributeError("Required struct cannot be None.")
            self._fields = {}
            return

        if not self._fields:
            self._fields = copy.deepcopy(self._schema)

        for name in value.keys():
            if name not in self._fields:
                raise AttributeError(
                    f"Field {name} doesn't exist in type {self.__class__.__name__}."
                )

        for name, field in self._fields.items():
            try:
                field.set(value.get(name, None))
            except AttributeError as e:
                raise AttributeError(
                    f"Error setting field {name} of {self.__class__.__name__}. {e}"
                )

    def get(self):
        """Get the value of the struct."""
        if not self._fields:
            return None

        outputs = {}
        for name, field in self._fields.items():
            try:
                outputs[name] = field.get()
            except AttributeError as e:
                raise AttributeError(
                    f"Error getting field {name} of {self.__class__.__name__}. {e}"
                )
        return outputs

    def validate(self, value: any):
        """
        Validate the value of the struct.

        Args:
            value (any): The value to be validated.

        Returns:
            any: The validated value.

        Raises:
            AttributeError: If the value is invalid.
        """
        if value is None:
            if not self._optional:
                raise AttributeError(f"Required struct cannot be None.")
            return None

        for name in value.keys():
            if name not in self._fields:
                raise AttributeError(
                    f"Field {name} doesn't exist in type {cls.__name__}."
                )

        outputs = {}
        for name, field in self._fields.items():
            try:
                outputs[name] = field.validate(value.get(name, None))
            except AttributeError as e:
                raise AttributeError(
                    f"Error validating field {name} of {self.__class__.__name__}. {e}"
                )
        return outputs

    def validate_field(self, name: str, value: any):
        """
        Validate a specific field in the struct.

        Args:
            name (str): The name of the field.
            value (any): The value to be validated.

        Returns:
            any: The validated value.

        Raises:
            AttributeError: If the field does not exist.
        """
        if name not in self._fields:
            raise AttributeError(
                f"Field {name} doesn't exist in type {self.__class__.__name__}."
            )
        return self._fields[name].validate(value)

    def __getattr__(self, name: str) -> any:
        """Get a field value by attribute name."""
        if name not in self._fields:
            raise AttributeError(
                f"Field {name} doesn't exist in type {self.__class__.__name__}."
            )
        return self._fields[name]

    def __setattr__(self, name: str, value: any):
        """Set a field value by attribute name."""
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            if name not in self._fields:
                raise AttributeError(
                    f"Field {name} doesn't exist in type {self.__class__.__name__}."
                )
            return self._fields[name].set(value)

    def __getitem__(self, name: str) -> any:
        """Get a field value by key name."""
        return self._fields[name]

    def __setitem__(self, name: str, value: any):
        """Set a field value by key name."""
        self._fields[name].set(value)

    def __delete__(self, name: str):
        """Delete a field by key name."""
        if self._fields[name].deletable:
            raise AttributeError(
                f"Can't delete required field {name} in type {self.__class__.__name__}."
            )
        self._fields[name].set(None)

    def __contains__(self, key):
        """Check if a key exists in the struct."""
        return key in self._fields

    def __len__(self):
        """Return the number of fields in the struct."""
        return len(self._fields)

    def __repr__(self):
        """Return a string representation of the struct."""
        return yaml.dump(self.get())

    def __str__(self):
        """Return a string representation of the struct."""
        return yaml.dump(self.get())

    def __deepcopy__(self, memo):
        """Return a deep copy of the struct."""
        return self.__class__(self._description, self._optional)

    def keys(self):
        """Return the keys of the struct."""
        return self._fields.keys()

    def items(self):
        """Return the items of the struct."""
        for name, field in self._fields.items():
            yield name, field.get()

    def lookup_flat(self, flat_key, sep="."):
        """
        Access an element with a flat key.

        Args:
            flat_key (str): The flat key string.
            sep (str): The separator character.

        Returns:
            any: The accessed element.

        Raises:
            AttributeError: If the element cannot be accessed.
        """
        p = self
        try:
            for k in flat_key.split(sep):
                p = p[k]
        except AttributeError as e:
            raise AttributeError(f"Error accessing {flat_key}. {e}")
        return p

    def set_flat(self, flat_key, val, sep="."):
        """
        Set an element with a flat key.

        Args:
            flat_key (str): The flat key string.
            val (any): The value to set.
            sep (str): The separator character.

        Raises:
            AttributeError: If the element cannot be set.
        """
        p = self
        keys = flat_key.split(sep)
        try:
            for k in keys[:-1]:
                p = p[k]
            p[keys[-1]] = val
        except AttributeError as e:
            raise AttributeError(f"Error setting {flat_key}. {e}")

    def read(path: str):
        """
        Create a Struct from a file.

        Args:
            path (str): The path to the file.

        Raises:
            RuntimeError: If the file extension is invalid.
        """
        ext = os.path.splitext(path)[1]
        if ext == ".json":
            self.set(json.load(open(path)))
        elif ext in [".yaml", ".yml"]:
            self.set(yaml.full_load(open(path)))
        else:
            raise RuntimeError(f"Invalid file extension {ext}.")

    def write(self, path: str):
        """
        Write the Struct to a file.

        Args:
            path (str): The path to the file.

        Raises:
            RuntimeError: If the file extension is invalid.
        """
        dirname = os.path.dirname(path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        if os.path.exists(path):
            print("Warning: Overriding config.")
        ext = os.path.splitext(path)[1]
        if ext == ".json":
            open(path, "w").write(json.dumps(self.get(), indent=4))
        elif ext in [".yaml", ".yml"]:
            open(path, "w").write(yaml.dump(self.get()))
        else:
            raise RuntimeError(f"Invalid file extension {ext}.")
