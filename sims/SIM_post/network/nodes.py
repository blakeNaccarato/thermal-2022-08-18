from __future__ import annotations

from math import pi
from pathlib import Path
from typing import TYPE_CHECKING, Mapping

import datadict
from pint import UnitRegistry

from gunns_sims import ContextDict

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparisonT

U = UnitRegistry(auto_reduce_dimensions=True, system="SI")
U.load_definitions(Path("units.txt"))
Q = U.Quantity


def main():

    Q.__repr__ = short_repr

    @datadict.dataclass
    class Node:
        pos: Q = Q(0, "in")

    diameter = Q(0.375, "in")
    cross_sectional_area = pi * diameter**2 / 4
    thermal_conductivity = Q(400, "W/(m*K)")
    flux = Q(60, "W/cm**2")
    rate = flux * cross_sectional_area

    init_nodes = dict(T5=0.950, T4=2.675, T3=3.150, T2=3.625, T1=4.100)
    nodes = ContextDict(
        {key: Node(Q(value, "in")) for key, value in init_nodes.items()}
    )
    nodes2 = {key: Node(Q(value, "in")) for key, value in init_nodes.items()}

    # links = sort_by_values(
    #     quantify(
    #         units="in",
    #         mapping=dict(
    #             boiling_surface=0.000,
    #             base=4.575,
    #         ),
    #     )
    # )

    collar_height = Q(1, "in")
    oring_thickness = Q(0.184, "in")
    floor_thickness = Q(0.75, "in")

    with nodes.context("pos"):
        nodes["upper_oring"] = nodes["T5"] - (collar_height / 2) - (oring_thickness / 2)
        nodes["lower_oring"] = nodes["T5"] + (collar_height / 2) - (oring_thickness / 2)
        nodes["chamber_floor"] = (
            nodes["T5"] + (collar_height / 2) + (floor_thickness / 2)
        )

    nodes = ContextDict(sorted(nodes.items(), key=lambda item: item[1].pos))
    ...
    # TODO: Define node and link dataclasses:
    # - Unpack the data above into them
    # - Supply on- and off-axis surface area at each node, node mass/volume
    # - Supply the off-axis insulation link properties (typical insulation, Kapton, PEEK)
    # - Supply the chamber link, just past the Kapton tape at the floor contact
    # - The chamber is a certain thermal mass with insulated outside walls and inside contact with water
    # - Each node will have thermal capacitance, and on-axis nodes will have off-axis insulation, and convective HT to air/water
    # - Finally, map the values computed here to their respective nodes and links in the GUNNS Draw.io network


# * -------------------------------------------------------------------------------- * #
# * QUANTITIES


def short_repr(self: Q):
    """Short representation of a quantity."""
    base = self.to_base_units()
    return f"{base.magnitude:#.3g} {base.units:~}"


def sort_by_values(
    mapping: Mapping[str, SupportsRichComparisonT]
) -> dict[str, SupportsRichComparisonT]:
    """Sort a mapping on its values."""
    return dict(sorted(mapping.items(), key=lambda item: item[1]))


# * -------------------------------------------------------------------------------- * #

if __name__ == "__main__":
    main()
    ...
