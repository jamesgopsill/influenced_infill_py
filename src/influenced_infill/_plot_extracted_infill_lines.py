from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator

from matplotlib import pyplot as plt

def plot_extracted_infill_lines(self: InfluencedInfillGenerator, n: int):
    for i, line in enumerate(self.vertical_infill_layer_lines[n]):
        plt.plot(line[:,0], line[:,1], "-b")
    for i, line in enumerate(self.diagonal_infill_layer_lines[n]):
        plt.plot(line[:,0], line[:,1], "-r")
    plt.title("Layer: "+str(n))
    plt.axis("equal")
    plt.savefig("extracted_infill.png", dpi=300)
    plt.clf()

