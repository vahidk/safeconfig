from typing import Any, Optional

from .field import _Field


class Variable(_Field):
    """Class representing a single variable field."""

    def __init__(
        self,
        data_type: type,
        description: Optional[str] = None,
        default: Optional[Any] = None,
        optional: bool = False,
    ):
        """
        Initialize a variable field.

        Args:
            data_type (type): The type of the variable.
            description (Optional[str]): Description of the variable.
            default (Optional[Any]): Default value of the variable.
            optional (bool): Whether the variable is optional.
        """
        self._value = None
        super().__init__(
            data_type=data_type,
            description=description,
            default=default,
            optional=optional,
        )

    def set(self, value: Any):
        """Set the value of the variable."""
        self._value = self.validate(value)

    def get(self) -> Any:
        """Get the value of the variable."""
        if self._value is None:
            if not self._optional:
                raise AttributeError("Required variable cannot be None.")
        return self._value

    def validate(self, value: Any) -> Any:
        """
        Validate the value of the variable.

        Args:
            value (Any): The value to be validated.

        Returns:
            Any: The validated value.

        Raises:
            AttributeError: If the value is None and the variable is required.
            ValueError: If the value is not of the expected data type.
        """
        if value is None:
            if self._default is None:
                if not self._optional:
                    raise AttributeError(f"Required variable cannot be None.")
                return None
            return self._default

        if not isinstance(value, self._data_type):
            raise ValueError(
                f"Invalid data type, expected {self._data_type.__name__}, got {type(value).__name__}"
            )
        return value

    def __repr__(self) -> str:
        """Return a string representation of the variable."""
        return str(self._value)

    def __str__(self) -> str:
        """Return a string representation of the variable."""
        return str(self._value)
