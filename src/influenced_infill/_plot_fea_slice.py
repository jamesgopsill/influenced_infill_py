from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator

from matplotlib import pyplot as plt
from numpy import max

def plot_fea_slice(self: InfluencedInfillGenerator, z: int):

    plt.pcolor(self.griddata[:,:,z], vmax=max(self.griddata) / 4)
    plt.colorbar()
    plt.savefig("griddata.png", dpi=300)
    plt.clf()

