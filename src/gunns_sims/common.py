from pathlib import Path
from typing import TypeAlias

from pint import Quantity, UnitRegistry

Q_num: TypeAlias = Quantity[float] | Quantity[int]

U = UnitRegistry(auto_reduce_dimensions=True, system="SI")
U.load_definitions(Path("units.txt"))
Q = U.Quantity


def short_repr(self: Q):
    """Short representation of a quantity."""
    base = self.to_base_units()
    return f"{base.magnitude:#.3g} {base.units:~}"


Q.__repr__ = short_repr
