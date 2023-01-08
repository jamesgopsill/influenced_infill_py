from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator

from matplotlib import pyplot as plt

def plot_influenced_infill_print_path(self: InfluencedInfillGenerator, layer: int):

    G = self.influenced_infill_networks[layer]
    
    for u, v, d in G.edges(data=True):
        p1 = G.nodes[u]["coords"]
        p2 = G.nodes[v]["coords"]
        if d["removable"]:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], "-b")
        elif d["travel_move"]:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], "--r", alpha=0.5)
        else:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], "-k")

    plt.title("Influenced Infill: "+str(layer))
    plt.axis("equal")
    plt.savefig("influenced_infill_print_paths.png", dpi=300)
    plt.clf()