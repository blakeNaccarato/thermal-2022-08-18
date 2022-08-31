from collections import UserDict
from contextlib import contextmanager
import dataclasses
from typing import Any, Protocol, TypeAlias, runtime_checkable


@runtime_checkable
class SupportsDataclass(Protocol):
    __dataclass_fields__: dict[str, Any]


# We could implement a protocol decorated with @runtime_checkable to check this
# properly. However, type checkers will always complain outside of runtime, since the
# methods that datadict adds (a special kind of dataclass) are dynamically added only at
# runtime. Instead, a simple type alias (which only checks for dataclass support but
# indicates that datadicts should be used) will suffice.
SupportsDataDict: TypeAlias = SupportsDataclass
"""Denotes a dataclass that should support dict-like item access.

Not enforced here, but by a separate protocol marked `@runtime_checkable` due to the
dynamic nature of dataclasses."""


@runtime_checkable
class SupportsDataDictAtRuntime(SupportsDataclass, Protocol):
    """Denotes a dataclass with dict-like item access.

    Enforced at runtime due to the dynamic nature of dataclasses."""

    def __getitem__(self, __k, __v):
        ...

    def __setitem__(self, __k, __v):
        ...


class ContextDict(UserDict[str, Any]):
    """Contextual attribute access on dataclass instances in dictionary values.

    Functions like a normal dictionary outside of the provided context manager. Dict
    values should be instances of a single dataclass that supports dict-like item
    access, such as a `datadict`.

    When using the context manager `ContextDict.context`, allows directly getting and
    setting the given field of the dataclasses in the values on key access without
    repeatedly calling that field. Nested contexts are supported.
    """

    def __init__(
        self,
        dict: dict[str, SupportsDataDict] | Any = None,  # noqa: A002
        **kwargs,
    ):
        self._context: str | None = None
        self._initialized = False
        super().__init__(dict, **kwargs)
        self.value_type = type(next(iter(self.values())))
        for value in self.values():
            self._validate_value(value)
        self._initialized = True

    def __getitem__(self, key: str) -> Any:
        value = super().__getitem__(key)
        return value[self._context] if self._context else value

    def __setitem__(self, key: str, item: Any):
        if self._context:
            value = super().__getitem__(key)
            value[self._context] = item
        else:
            if self._initialized:
                self._validate_value(item)
            super().__setitem__(key, item)

    def __missing__(self, key: str) -> Any:
        """Return a new instance of the dataclass when a key is missing."""
        super().__setitem__(key, self.value_type())
        return super().__getitem__(key)

    @contextmanager
    def context(self, context: str):
        """Enter a context where certain fields can be accessed."""
        self._validate_context(context)
        previous_context = self._context
        try:
            self._context = context
            yield
        finally:
            self._context = previous_context

    def _validate_context(self, context: str):
        """Ensure that the field provided is one of the fields of the dataclass."""
        if context not in (field.name for field in dataclasses.fields(self.value_type)):
            raise ValueError(
                f"Provided context '{context}' is not a field of {self.value_type}"
            )

    def _validate_value(self, value):
        """Validate a dict value.

        Check whether a value is an instance of the expected dataclass, and whether that
        dataclass supports dict-like item access."""

        if not isinstance(value, SupportsDataclass):
            raise ValueError("Values must be dataclasses." f"\n\tGot: {type(value)}")
        if not isinstance(value, self.value_type):
            raise ValueError(
                "Values must be instances of the same dataclass."
                f"\n\tExpected: {self.value_type}"
                f"\n\tGot: {type(value)}"
            )
        if not isinstance(value, SupportsDataDictAtRuntime):
            raise TypeError(
                "Values must be dataclasses that support dict-like item access."
                f"\n\tClass {type(value)} does not appear to support dict-like item access."
            )
