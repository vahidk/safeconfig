from abc import ABC, abstractmethod
from typing import Optional


class _Field(ABC):
    """Abstract base class for all configuration fields."""

    def __init__(
        self,
        data_type: type,
        description: Optional[str] = None,
        default: Optional[any] = None,
        optional: bool = False,
    ):
        """
        Initialize a field with data type, description, default value, and optionality.

        Args:
            data_type (type): The type of the field.
            description (Optional[str]): Description of the field.
            default (Optional[any]): Default value of the field.
            optional (bool): Whether the field is optional.
        """
        self._data_type = data_type
        self._description = description
        self._default = None
        self._optional = optional
        if default is not None:
            self._default = self.validate(default)

    @property
    def data_type(self) -> str:
        """Return the data type of the field."""
        return self._data_type

    @property
    def description(self) -> str:
        """Return the description of the field."""
        return self._description

    @property
    def optional(self) -> bool:
        """Return whether the field is optional."""
        return self._optional

    @property
    def default(self) -> str:
        """Return the default value of the field."""
        return self._default

    @property
    def deletable(self) -> bool:
        """Return whether the field is deletable."""
        return self._optional or self._default is not None

    @abstractmethod
    def set(self, value: any):
        """Set the value of the field."""
        pass

    @abstractmethod
    def get(self) -> any:
        """Get the value of the field."""
        pass

    @abstractmethod
    def validate(self, value: any) -> any:
        """Validate the value of the field."""
        pass
