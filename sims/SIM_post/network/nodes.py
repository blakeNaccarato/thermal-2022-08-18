from __future__ import annotations

from collections import UserDict
import dataclasses
from math import pi
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping, Protocol, TypeAlias, runtime_checkable

from pint import UnitRegistry
from typing_extensions import dataclass_transform

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparisonT

U = UnitRegistry(auto_reduce_dimensions=True, system="SI")
U.load_definitions(Path("units.txt"))
Q = U.Quantity


def main():

    Q.__repr__ = short_repr

    diameter = Q(0.375, "in")
    cross_sectional_area = pi * diameter**2 / 4
    thermal_conductivity = Q(400, "W/(m*K)")
    flux = Q(60, "W/cm**2")
    rate = flux * cross_sectional_area

    nodes = quantify(
        units="in",
        mapping=ContextDict(
            dict(
                T5=Node(pos=(0.950, 0)),
                T4=Node(pos=(2.675, 0)),
                T3=Node(pos=(3.150, 0)),
                T2=Node(pos=(3.625, 0)),
                T1=Node(pos=(4.100, 0)),
            ),
        ),
    )

    links = sort_by_values(
        quantify(
            units="in",
            mapping=dict(
                boiling_surface=0.000,
                base=4.575,
            ),
        )
    )

    collar_height = Q(1, "in")
    oring_thickness = Q(0.184, "in")
    floor_thickness = Q(0.75, "in")

    nodes["upper_oring"] = nodes["T5"] - (collar_height / 2) - (oring_thickness / 2)
    nodes["lower_oring"] = nodes["T5"] + (collar_height / 2) - (oring_thickness / 2)
    nodes["chamber_floor"] = nodes["T5"] + (collar_height / 2) + (floor_thickness / 2)

    nodes = sort_by_values(nodes)

    # TODO: Define node and link dataclasses:
    # - Unpack the data above into them
    # - Supply on- and off-axis surface area at each node, node mass/volume
    # - Supply the off-axis insulation link properties (typical insulation, Kapton, PEEK)
    # - Supply the chamber link, just past the Kapton tape at the floor contact
    # - The chamber is a certain thermal mass with insulated outside walls and inside contact with water
    # - Each node will have thermal capacitance, and on-axis nodes will have off-axis insulation, and convective HT to air/water
    # - Finally, map the values computed here to their respective nodes and links in the GUNNS Draw.io network
    ...


# * -------------------------------------------------------------------------------- * #
# * DATADICT
# In-lining this implementation for now.
# See: https://github.com/gahjelle/datadict/issues/1


@dataclass_transform()
def datadict(cls=None, **kwargs):
    """Add item access to attributes"""

    def wrap(cls):
        """Wrapper that adds methods and attributes to class"""

        # Create regular dataclass
        cls = dataclasses.dataclass(**kwargs)(cls)

        # Add item access
        dataclasses._set_new_attribute(cls, "__getitem__", _getitem)  # type: ignore
        dataclasses._set_new_attribute(cls, "__setitem__", _setitem)  # type: ignore
        dataclasses._set_new_attribute(cls, "__delitem__", _delitem)  # type: ignore
        dataclasses._set_new_attribute(cls, "asdict", _asdict)  # type: ignore

        return cls

    return wrap if cls is None else wrap(cls)


def _getitem(self, key):
    """Get an attribute from a dataclass using item access"""
    try:
        return getattr(self, key)
    except AttributeError:
        raise KeyError(key) from None


def _setitem(self, key, value):
    """Set an attribute on a dataclass using item access"""
    setattr(self, key, value)


def _delitem(self, key):
    """Delete an attribute on a dataclass using item access"""
    delattr(self, key)


def _asdict(self):
    """Convert the dataclass to a dictionary"""
    return dataclasses.asdict(self)


# * -------------------------------------------------------------------------------- * #
# * CONTEXTUAL DATA DICT


class SupportsDataclass(Protocol):
    __dataclass_fields__: dict[str, Any]


# We could implement a protocol decorated with @runtime_checkable to check this
# properly. However, type checkers will always complain outside of runtime, since the
# methods that datadict adds (a special kind of dataclass) are dynamically added only at
# runtime. Instead, a simple type alias (which only checks for dataclass support but
# indicates that datadicts should be used) will suffice.
MustBeDataDict: TypeAlias = SupportsDataclass
"""User must supply a dataclass that supports dict-like item access. Can only be
enforced at runtime due to dynamic nature of dataclasses."""


@runtime_checkable
class SupportsDataDict(SupportsDataclass, Protocol):
    """Support for a dataclass with dict-like item access."""

    def __getitem__(self, __k, __v):
        ...

    def __setitem__(self, __k, __v):
        ...


class ContextDict(UserDict[str, Any]):
    """Contextual attribute access on dataclass instances in dictionary values.

    Inside a context manager, allows getting and setting certain fields on key access
    without explicitly calling those fields. Outside of a context manager, just get and
    set the dataclass instances themselves upon key access. Dict values must be
    instances of a given dataclass.
    """

    def __init__(
        self,
        dict: dict[str, MustBeDataDict] | None = None,  # noqa: A002
        **kwargs,
    ):
        super().__init__(dict, **kwargs)
        self.value_type = type(next(iter(self.values())))
        self.validate()

    def validate(self):
        """Validate dict values.

        Check whether all values are instances of the same dataclass, and whether
        that dataclass supports dict-like item access."""

        for value in self.values():
            exc_details = f"\n\tOffending value:\n\t{value}"
            if not isinstance(value, SupportsDataDict):
                raise TypeError(
                    f"Values must be dataclasses that support dict-like item access.{exc_details}"
                )
            if not isinstance(value, self.value_type):
                raise ValueError(
                    f"Values must be instances of the same dataclass.{exc_details}"
                )


@dataclasses.dataclass
class Node:
    label: str = ""
    pos: tuple[float, float] = (0, 0)


context_dict = ContextDict(
    hello=Node("well", (0, 0)),
    world=Node("quell", (1, 1)),
)
...

# * -------------------------------------------------------------------------------- * #
# * QUANTITIES


def short_repr(self: Q):
    """Short representation of a quantity."""
    base = self.to_base_units()
    return f"{base.magnitude:#.3g} {base.units:~}"


def quantify(mapping: Mapping[str, Any], units: str) -> dict[str, Q]:
    """Quantify the values of a mapping."""
    return {key: Q(value, units) for key, value in mapping.items()}


def sort_by_values(
    mapping: Mapping[str, SupportsRichComparisonT]
) -> dict[str, SupportsRichComparisonT]:
    """Sort a mapping on its values."""
    return dict(sorted(mapping.items(), key=lambda item: item[1]))


# * -------------------------------------------------------------------------------- * #

if __name__ == "__main__":
    main()
    ...
