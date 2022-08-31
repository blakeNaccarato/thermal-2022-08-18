from math import nan

import datadict

from gunns_sims.common import Q, Q_num

# * -------------------------------------------------------------------------------- * #
# * COMMON


@datadict.dataclass
class Labelled:
    label: str = ""


# * -------------------------------------------------------------------------------- * #
# * NODES AND LINKS


@datadict.dataclass
class Node(Labelled):
    axial_pos: Q_num = Q(nan)
    radial_pos: Q_num = Q(nan)
    mass: Q_num = Q(nan)


@datadict.dataclass
class Conductor(Labelled):
    length: Q_num = Q(nan)
    area: Q_num = Q(nan)
    thermal_conductivity: Q_num = Q(nan)

    @property
    def conductance(self) -> Q_num:
        return self.length / self.thermal_conductivity / self.area


# * -------------------------------------------------------------------------------- * #
# * BOUNDARIES


@datadict.dataclass
class Heater(Labelled):
    flux: Q_num = Q(nan)


@datadict.dataclass
class Potential(Labelled):
    temperature: Q_num = Q(nan)
