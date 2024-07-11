import copy
import json
import os
from typing import Any, Optional

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

    def __init__(
        self,
        description: Optional[str] = None,
        default: Optional[Any] = None,
        optional: bool = False,
    ):
        """
        Initialize a structured field.

        Args:
            description (Optional[str]): Description of the struct.
            default (Optional[Any]): Default value of the variable.
            optional (bool): Whether the struct is optional.
        """
        if self.__class__ == Struct:
            raise TypeError("Struct class cannot be instantiated directly.")
        self._fields: dict = {}
        super().__init__(
            data_type=self.__class__,
            description=description,
            default=default,
            optional=optional,
        )

    def set(self, value: Any):
        """
        Set the value of the struct.

        Args:
            value (Any): The value to be set.

        Raises:
            AttributeError: If the value is invalid.
        """
        if value is None:
            if self._default is None:
                if not self._optional:
                    raise AttributeError("Required struct cannot be None.")
                self._fields = {}
                return
            value = self._default

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

    def get(self) -> Any:
        """Get the value of the struct."""
        if not self._fields:
            if not self._optional:
                raise AttributeError("Required struct cannot be None.")
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

    def validate(self, value: Any) -> Any:
        """
        Validate the value of the struct.

        Args:
            value (Any): The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            AttributeError: If the value is invalid.
        """
        if value is None:
            if self._default is None:
                if not self._optional:
                    raise AttributeError("Required struct cannot be None.")
                return None
            return self._default

        for name in value.keys():
            if name not in self._schema:
                raise AttributeError(
                    f"Field {name} doesn't exist in type {self.__class__.__name__}."
                )

        outputs = {}
        for name, field in self._schema.items():
            try:
                outputs[name] = field.validate(value.get(name, None))
            except AttributeError as e:
                raise AttributeError(
                    f"Error validating field {name} of {self.__class__.__name__}. {e}"
                )
        return outputs

    def __getattr__(self, name: str) -> Any:
        """Get a field value by attribute name."""
        if name not in self._fields:
            raise AttributeError(
                f"Field {name} doesn't exist in type {self.__class__.__name__}."
            )
        return self._fields[name]

    def __setattr__(self, name: str, value: Any):
        """Set a field value by attribute name."""
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            if name not in self._fields:
                raise AttributeError(
                    f"Field {name} doesn't exist in type {self.__class__.__name__}."
                )
            return self._fields[name].set(value)

    def __getitem__(self, name: str) -> Any:
        """Get a field value by key name."""
        return self._fields[name]

    def __setitem__(self, name: str, value: Any):
        """Set a field value by key name."""
        self._fields[name].set(value)

    def __delete__(self, name: str):
        """Delete a field by key name."""
        field = self._fields[name]
        if field._optional or field._default is not None:
            raise AttributeError(
                f"Can't delete required field {name} in type {self.__class__.__name__}."
            )
        field.set(None)

    def __contains__(self, key) -> bool:
        """Check if a key exists in the struct."""
        return key in self._fields

    def __len__(self) -> int:
        """Return the number of fields in the struct."""
        return len(self._fields)

    def __repr__(self) -> str:
        """Return a string representation of the struct."""
        return yaml.dump(self.get())

    def __str__(self) -> str:
        """Return a string representation of the struct."""
        return yaml.dump(self.get())

    def __deepcopy__(self, memo: Any) -> Any:
        """Return a deep copy of the struct."""
        return self.__class__(
            description=self._description,
            default=self._default,
            optional=self._optional,
        )

    def keys(self) -> Any:
        """Return the keys of the struct."""
        return self._fields.keys()

    def items(self) -> Any:
        """Return the items of the struct."""
        for name, field in self._fields.items():
            yield name, field.get()

    def get_flat(self, flat_key: str, sep: str = ".") -> Any:
        """
        Access an element with a flat key.

        Args:
            flat_key (str): The flat key string.
            sep (str): The separator character.

        Returns:
            Any: The accessed element.

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

    def set_flat(self, flat_key: str, val: Any, sep: str = "."):
        """
        Set an element with a flat key.

        Args:
            flat_key (str): The flat key string.
            val (Any): The value to set.
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

    def read(self, path: str) -> Any:
        """
        Create a Struct from a file.

        Args:
            path (str): The path to the file.

        Raises:
            RuntimeError: If the file extension is invalid.
        """
        ext = os.path.splitext(path)[1]
        if ext == ".json":
            with open(path, "r") as file:
                self.set(json.load(file))
        elif ext in [".yaml", ".yml"]:
            with open(path, "r") as file:
                self.set(yaml.full_load(file))
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
            with open(path, "w") as file:
                file.write(json.dumps(self.get(), indent=4))
        elif ext in [".yaml", ".yml"]:
            with open(path, "w") as file:
                file.write(yaml.dump(self.get()))
        else:
            raise RuntimeError(f"Invalid file extension {ext}.")
