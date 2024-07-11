from abc import ABC, abstractmethod
from typing import Any, Optional


class _Field(ABC):
    """Abstract base class for all configuration fields."""

    def __init__(
        self,
        data_type: type,
        description: Optional[str] = None,
        default: Optional[Any] = None,
        optional: bool = False,
    ):
        """
        Initialize a field with data type, description, default value, and optionality.

        Args:
            data_type (type): The type of the field.
            description (Optional[str]): Description of the field.
            default (Optional[Any]): Default value of the field.
            optional (bool): Whether the field is optional.
        """
        self._data_type = data_type
        self._description = description
        self._default = None
        self._optional = optional
        if default is not None:
            self._default = self.validate(default)
            self.set(default)

    @property
    def data_type(self) -> type:
        """Return the data type of the field."""
        return self._data_type

    @property
    def description(self) -> Optional[str]:
        """Return the description of the field."""
        return self._description

    @property
    def optional(self) -> bool:
        """Return whether the field is optional."""
        return self._optional

    @property
    def default(self) -> Optional[Any]:
        """Return the default value of the field."""
        return self._default

    @abstractmethod
    def set(self, value: Any):
        """Set the value of the field."""
        pass

    @abstractmethod
    def get(self) -> Any:
        """Get the value of the field."""
        pass

    @abstractmethod
    def validate(self, value: Any) -> Any:
        """Validate the value of the field."""
        pass
