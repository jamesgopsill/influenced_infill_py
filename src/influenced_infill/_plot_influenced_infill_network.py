from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator

from matplotlib import pyplot as plt

def plot_influenced_infill_network(self: InfluencedInfillGenerator, i: int):
    G = self.influenced_infill_networks[i]
    if G == None:
        print("No network for this layer")
        return
    for u, v, d in G.edges(data=True):
        p1 = G.nodes[u]["coords"]
        p2 = G.nodes[v]["coords"]
        if d["removable"]:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], "-b")
        else:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], "-k")
    for n, d in G.nodes(data=True):
        plt.plot(d["coords"][0], d["coords"][1], ".b")
    plt.title("Network: "+str(i))
    plt.axis("equal")
    plt.savefig("network.png", dpi=300)
    plt.clf()