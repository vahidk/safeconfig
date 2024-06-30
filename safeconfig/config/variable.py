from typing import Optional

from .field import _Field


class Variable(_Field):
    """Class representing a single variable field."""

    def __init__(
        self,
        data_type: type,
        description: Optional[str] = None,
        default: Optional[any] = None,
        optional: bool = False,
    ):
        """
        Initialize a variable field.

        Args:
            data_type (type): The type of the variable.
            description (Optional[str]): Description of the variable.
            default (Optional[any]): Default value of the variable.
            optional (bool): Whether the variable is optional.
        """
        self._value = None
        super().__init__(
            data_type=data_type,
            description=description,
            default=default,
            optional=optional,
        )

    def set(self, value: any):
        """Set the value of the variable."""
        self._value = self.validate(value)

    def get(self):
        """Get the value of the variable."""
        if self._value is None:
            if not self._optional:
                raise AttributeError("Required variable cannot be None.")
        return self._value

    def validate(self, value: any):
        """
        Validate the value of the variable.

        Args:
            value (any): The value to be validated.

        Returns:
            any: The validated value.

        Raises:
            AttributeError: If the value is None and the variable is required.
            ValueError: If the value is not of the expected data type.
        """
        if value is None:
            if self._default is None:
                if not self._optional:
                    raise AttributeError(f"Required variable cannot be None.")
                return None
            value = self._default
        if not isinstance(value, self._data_type):
            raise ValueError(
                f"Invalid data type, expected {self._data_type.__name__}, got {type(value).__name__}"
            )
        return value

    def __repr__(self):
        """Return a string representation of the variable."""
        return str(self._value)

    def __str__(self):
        """Return a string representation of the variable."""
        return str(self._value)
