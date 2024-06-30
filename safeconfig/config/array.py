from typing import Optional

from .field import _Field
from .variable import Variable


class Array(_Field):
    """Class representing an array field."""

    def __init__(
        self,
        data_type: type,
        description: Optional[str] = None,
        default: Optional[any] = None,
        optional: bool = False,
    ):
        """
        Initialize an array field.

        Args:
            data_type (type): The type of elements in the array.
            description (Optional[str]): Description of the array.
            default (Optional[any]): Default value of the array.
            optional (bool): Whether the array is optional.
        """
        if issubclass(data_type, _Field):
            self._create_field = lambda: data_type()
        else:
            self._create_field = lambda: Variable(data_type=data_type)
        self._validate_field = self._create_field().validate
        self._values = None
        super().__init__(
            data_type=data_type,
            description=description,
            default=default,
            optional=optional,
        )

    def set(self, value: any):
        """
        Set the value of the array.

        Args:
            value (any): The value to be set.

        Raises:
            AttributeError: If the value is invalid.
        """
        if value is None:
            if self._default is None:
                if not self._optional:
                    raise AttributeError(f"Required array cannot be None.")
                self._values = None
                return
            value = self._default

        output = []
        for i, v in enumerate(value):
            field = self._create_field()
            try:
                field.set(v)
            except AttributeError as e:
                raise AttributeError(f"Error setting {i}th element of array. {e}")
            output.append(field)
        self._values = output

    def get(self):
        """Get the value of the array."""
        if self._values is None:
            if not self._optional:
                raise AttributeError(f"Required array cannot be None.")
            return None

        outputs = []
        for i, v in enumerate(self._values):
            try:
                outputs.append(v.get())
            except AttributeError as e:
                raise AttributeError(f"Error getting {i}th element of array. {e}")
        return outputs

    def validate(self, value: any):
        """
        Validate the value of the array.

        Args:
            value (any): The value to be validated.

        Returns:
            any: The validated value.

        Raises:
            AttributeError: If the value is invalid.
        """
        if value is None:
            if self._default is None:
                if not self._optional:
                    raise AttributeError(f"Required array cannot be None.")
                return None
            value = self._default

        outputs = []
        for i, v in enumerate(value):
            try:
                outputs.append(self._validate_field(v))
            except AttributeError as e:
                raise AttributeError(f"Error validating {i}th element of array. {e}")
        return outputs

    def __getitem__(self, idx: int) -> any:
        """Get an item from the array by index."""
        return self._values[idx]

    def __setitem__(self, idx: int, value: any):
        """Set an item in the array by index."""
        self._values[idx].set(value)

    def __delete__(self, idx: int):
        """Delete an item from the array by index."""
        del self._values[idx]

    def __contains__(self, value: any):
        """Check if a value is in the array."""
        return value in self._values

    def __len__(self):
        """Return the length of the array."""
        return len(self._values)

    def __repr__(self):
        """Return a string representation of the array."""
        return yaml.dump(self.get())

    def __str__(self):
        """Return a string representation of the array."""
        return yaml.dump(self.get())

    def append(self, value: any):
        """Append a value to the array."""
        field = self._create_field()
        field.set(value)
        self._values.append(field)

    def extend(self, values: list):
        """Extend the array with a list of values."""
        for value in values:
            self.append(value)

    def pop(self, idx: Optional[int] = None):
        """Pop a value from the array by index."""
        return self._values.pop(idx)
