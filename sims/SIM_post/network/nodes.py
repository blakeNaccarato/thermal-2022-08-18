from __future__ import annotations
from collections import UserDict

from typing import TYPE_CHECKING, Any, Mapping, Protocol, TypeVar

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparisonT, SupportsItemAccess

import dataclasses
from math import pi
from pathlib import Path

from pint import UnitRegistry
from typing_extensions import dataclass_transform

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
        mapping=ContextualDataclass(
            dict(
                T5=(0.950, 0),
                T4=(2.675, 0),
                T3=(3.150, 0),
                T2=(3.625, 0),
                T1=(4.100, 0),
            ),
            Node,
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


class SupportsDataclass(Protocol):
    __dataclass_fields__: dict[str, Any]


_VT = TypeVar("_VT")


class SupportsDataclassAndItemAccess(
    SupportsItemAccess[str, _VT], SupportsDataclass, Protocol[_VT]
):
    ...


# TODO: Implement SupportsGetAttr or use appropriate ABC, make sure the type annotation
# below, UserDict[str, SupportsDataclass], also checks that __getitem__ is implemented.


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


# TODO: Implement SupportsGetAttr or use appropriate ABC, make sure the type annotation
# below, UserDict[str, SupportsDataclass], also checks that __getitem__ is implemented.


class ContextualDataclass(UserDict[str, SupportsDataclassAndItemAccess[Any]]):
    """Contextual attribute access on dataclass instances in dictionary values.

    Inside a context manager, allows getting and setting certain fields on key access
    without explicitly calling those fields. Outside of a context manager, just get and
    set the dataclass instances themselves upon key access. Dict values must be
    instances of a given dataclass.
    """

    def __init__(
        self,
        dict: dict[str, Any],  # noqa: A002s
        dataclass_context: SupportsDataclass,
        **kwargs,
    ):
        super().__init__(dict, **kwargs)
        self.dataclass_context = dataclass_context


@datadict
class Node:
    pos: tuple[float, float]


test = ContextualDataclass(dict(hello=Node((0, 0))), Node)

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
