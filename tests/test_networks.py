import pytest

from gunns_sims.classes import Node
from gunns_sims.common import Q
from gunns_sims.contextdict import ContextDict
from gunns_sims.networks import get_mass_of_chain


@pytest.mark.parametrize(
    "label,total_length,nodes,expected",
    [
        (
            "equal",
            Q(4),
            ContextDict(
                {
                    "a": Node(axial_pos=Q(1)),
                    "b": Node(axial_pos=Q(2)),
                    "c": Node(axial_pos=Q(3)),
                }
            ),
            ContextDict(
                {
                    "a": Node(mass=Q(1.5)),
                    "b": Node(mass=Q(1)),
                    "c": Node(mass=Q(1.5)),
                }
            ),
        ),
        (
            "unequal",
            Q(16),
            ContextDict(
                {
                    "a": Node(axial_pos=Q(1)),
                    "b": Node(axial_pos=Q(4)),
                    "c": Node(axial_pos=Q(9)),
                }
            ),
            ContextDict(
                {
                    "a": Node(mass=Q(2.5)),
                    "b": Node(mass=Q(4)),
                    "c": Node(mass=Q(9.5)),
                }
            ),
        ),
    ],
)
def test_get_mass_of_chain(label, total_length, nodes, expected):
    cross_sectional_area = Q(1)
    density = Q(1)

    nodes = get_mass_of_chain(nodes, total_length, cross_sectional_area, density)

    total_mass = total_length * cross_sectional_area * density
    with nodes.context("mass"), expected.context("mass"):
        for key in nodes.keys():
            assert nodes[key] == expected[key]
        assert sum(nodes.values()) == total_mass
