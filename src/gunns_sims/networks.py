from gunns_sims.common import Q_num
from gunns_sims.contextdict import ContextDict


def get_mass_of_chain(nodes, post_total_length, cross_sectional_area, density):
    nodes = ContextDict(sorted(nodes.items(), key=lambda item: item[1].axial_pos))

    def get_cylindrical_node_mass(length: Q_num) -> Q_num:
        return length * cross_sectional_area * density

    with nodes.context("axial_pos"):
        pos = list(nodes.values())
        pos.append(post_total_length)

    with nodes.context("mass"):
        remaining_keys = iter(nodes.keys())
        first_key = next(remaining_keys)
        nodes[first_key] = get_cylindrical_node_mass(pos[1] / 2 - pos[0])
        for key, prev_pos, next_pos in zip(remaining_keys, pos[:-1], pos[2:]):
            nodes[key] = get_cylindrical_node_mass((next_pos - prev_pos) / 2)
        last_key = list(nodes.keys())[-1]
        nodes[last_key] = get_cylindrical_node_mass(pos[-1] - pos[-3] / 2)

    total_mass = get_cylindrical_node_mass(post_total_length)
    return nodes
