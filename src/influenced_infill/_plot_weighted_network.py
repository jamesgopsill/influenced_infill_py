from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator

from matplotlib import pyplot as plt
from numpy import max

def plot_weighted_network(self: InfluencedInfillGenerator, i: int):
    G = self.influenced_infill_networks[i]
    max_stress = max(self.griddata) * 0.25
    if G == None:
        print("No network for this layer")
        return
    for u, v, d in G.edges(data=True):
        p1 = G.nodes[u]["coords"]
        p2 = G.nodes[v]["coords"]
        if d["removable"]:
            alpha = d["w"] / max_stress
            if alpha > 1: alpha = 1
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], "-b", alpha=alpha)
        else:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], "-k")
    plt.title("Network: "+str(i))
    plt.axis("equal")
    plt.savefig("weighted_network.png", dpi=300)
    plt.clf()