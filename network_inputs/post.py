from __future__ import annotations

from math import pi
from typing import TYPE_CHECKING, Mapping
from gunns_sims.classes import Node
from gunns_sims.common import Q, orig_repr

from gunns_sims.contextdict import ContextDict
from gunns_sims.networks import get_mass_of_chain

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparisonT

Q.__repr__ = orig_repr


def main():

    post_diameter = Q(0.375, "in")
    post_cross_sectional_area = pi * post_diameter**2 / 4
    post_density = Q(8.96, "g/cm^3")
    post_thermal_conductivity = Q(400, "W/(m*K)")
    post_total_length = Q(4.575, "in")

    node_lengths_inch = dict(T5=0.950, T4=2.675, T3=3.150, T2=3.625, T1=4.100)
    nodes = ContextDict(
        {
            key: Node(axial_pos=Q(value, "in"))
            for key, value in node_lengths_inch.items()
        }
    )

    collar_height = Q(1, "in")
    oring_thickness = Q(0.184, "in")
    floor_thickness = Q(0.75, "in")

    with nodes.context("axial_pos"):
        nodes["upper_oring"] = nodes["T5"] - (collar_height / 2) - (oring_thickness / 2)
        nodes["lower_oring"] = nodes["T5"] + (collar_height / 2) - (oring_thickness / 2)
        nodes["chamber_floor"] = (
            nodes["T5"] + (collar_height / 2) + (floor_thickness / 2)
        )

    with nodes.context("radial_pos"):
        for key in nodes.keys():
            nodes[key] = Q(0, "in")

    nodes = get_mass_of_chain(
        nodes, post_total_length, post_cross_sectional_area, post_density
    )

    ...

    # TODO: Define node and link dataclasses:
    # - Unpack the data above into them
    # - Supply on- and off-axis surface area at each node, node mass/volume
    # - Supply the off-axis insulation link properties (typical insulation, Kapton, PEEK)
    # - Supply the chamber link, just past the Kapton tape at the floor contact
    # - The chamber is a certain thermal mass with insulated outside walls and inside contact with water
    # - Each node will have thermal capacitance, and on-axis nodes will have off-axis insulation, and convective HT to air/water
    # - Finally, map the values computed here to their respective nodes and links in the GUNNS Draw.io network

    # heater = Heater(label="base", flux=Q(60, "W/cm**2"))
    # boiling_surface = Potential(label="boiling surface", temperature=Q(100, "C"))
    # ambient = Potential(label="ambient", temperature=Q(25, "C"))
    # conductors = ContextDict(Conductor(length=Q(0, "in")) for _ in range(1, len(nodes)))


# * -------------------------------------------------------------------------------- * #
# * QUANTITIES


def sort_by_values(
    mapping: Mapping[str, SupportsRichComparisonT]
) -> dict[str, SupportsRichComparisonT]:
    """Sort a mapping on its values."""
    return dict(sorted(mapping.items(), key=lambda item: item[1]))


# * -------------------------------------------------------------------------------- * #

if __name__ == "__main__":
    main()
    ...
