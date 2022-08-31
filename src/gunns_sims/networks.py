from gunns_sims.common import Q_num
from gunns_sims.contextdict import ContextDict


def get_mass_of_chain(
    nodes: ContextDict,
    total_length: Q_num,
    cross_sectional_area: Q_num,
    density: Q_num,
) -> ContextDict:
    """Get the mass of each node in a chain of nodes.

    Internal nodes take half the mass between themselves and each of their neighbors.
    Boundary nodes take half the mass between themselves and their single neighbor, and
    the entire mass opposite their neighbor.
    """

    nodes_sorted = ContextDict(
        sorted(nodes.items(), key=lambda item: item[1].axial_pos)
    )

    def get_cylindrical_node_mass(length: Q_num) -> Q_num:
        return length * cross_sectional_area * density

    total_mass = get_cylindrical_node_mass(total_length)

    with nodes_sorted.context("axial_pos"):
        running_total_mass = [
            get_cylindrical_node_mass(node) for node in nodes_sorted.values()
        ]

    running_total_mass_prev = [0, *running_total_mass[:-1]]
    running_total_mass_next = [*running_total_mass[1:], total_mass]

    with nodes_sorted.context("mass"):
        for i, (n, mass_up_to_prev, mass_up_to_self, mass_up_to_next) in enumerate(
            zip(
                nodes_sorted,
                running_total_mass_prev,
                running_total_mass,
                running_total_mass_next,
            )
        ):
            if i == 0:
                # First node
                nodes_sorted[n] = (
                    mass_up_to_self + (mass_up_to_next - mass_up_to_self) / 2
                )
            elif i == len(nodes_sorted) - 1:
                # Last node
                nodes_sorted[n] = (mass_up_to_self - mass_up_to_prev) / 2 + (
                    mass_up_to_next - mass_up_to_self
                )
            else:
                # Internal nodes
                nodes_sorted[n] = (mass_up_to_next - mass_up_to_prev) / 2

    return nodes | nodes_sorted  # type: ignore
