from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator
    
from numpy import arange
from numpy.random import shuffle

def generate_influenced_infill(self: InfluencedInfillGenerator, threshold: float):
    print("Generating Influenced Infill")
    for i, G in enumerate(self.influenced_infill_networks):
        if G == None:
            continue

        ebunch = []
        for u, v, d in G.edges(data=True):
            if d["removable"] and d["w"] < threshold:
                ebunch.append((u, v))
        G.remove_edges_from(ebunch)

        nbunch = []
        for n in G.nodes():
            if G.degree(n) == 0:
                nbunch.append(n)

        G.remove_nodes_from(nbunch)

        odd_nodes = []
        for n in G.nodes():
            if G.degree(n) % 2 != 0: # if the degree is odd
                odd_nodes.append(n)

        print("# Odd Nodes:", len(odd_nodes))

        paired_off = False
        paired_off_count = 0
        # Create the pairing
        while paired_off == False:
            shuffle(odd_nodes)
            paired_off = True
            for j in arange(0, len(odd_nodes), 2):
                u = odd_nodes[j]
                v = odd_nodes[j+1]
                if G.has_edge(u, v):
                    paired_off = False
            if paired_off_count > 50:
                print("Could not pair off.")
                break
            paired_off_count += 1

        # Perform the pairing
        for j in arange(0, len(odd_nodes), 2):
            G.add_edge(
                odd_nodes[j], 
                odd_nodes[j+1], 
                w=None, 
                removable=False, 
                travel_move=True
            )