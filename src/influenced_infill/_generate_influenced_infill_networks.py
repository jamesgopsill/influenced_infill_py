from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator

from networkx import Graph
from numpy import round, unique, asarray, append
from numpy.linalg import norm

def intersect(l1, l2):
    x1,y1 = l1[0]
    x2,y2 = l1[1]
    x3,y3 = l2[0]
    x4,y4 = l2[1]
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0: # parallel
        return None, None
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    if ua < 0 or ua > 1: # out of range
        return None, None
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    if ub < 0 or ub > 1: # out of range
        return None, None
    x = x1 + ua * (x2-x1)
    y = y1 + ua * (y2-y1)
    return x, y

def generate_influenced_infill_networks(self: InfluencedInfillGenerator, start_on_layer: int, end_on_layer: int):

    self.influenced_infill_networks = []
    n_layers = len(self.vertical_infill_layer_lines)
    for i in range(0, n_layers):
        if i >= start_on_layer and i <= end_on_layer:
            G = self.generate_influenced_infill_network(i)
            self.influenced_infill_networks.append(G)
        else:
            self.influenced_infill_networks.append(None)

def generate_influenced_infill_network(self: InfluencedInfillGenerator, layer: int):

    G = Graph()
    print(G.number_of_nodes(), G.number_of_edges())

    points_of_points = []
    for l1 in self.vertical_infill_layer_lines[layer]:
        
        # Gather the intersecting points along l1's path
        points = []
        for l2 in self.diagonal_infill_layer_lines[layer]:
            x, y = intersect(l1, l2)
            if x:
                points.append([round(x, 1), round(y, 1)])
        
        points = asarray(points)
        if len(points) > 0:
            for p in l1:
                if not any((points[:]==p).all(1)):
                    points = append(points, [round(p, 1)], axis=0)
        else:
            points = l1
        points = points[points[:, 0].argsort()]
        points = points[points[:, 1].argsort()]
        points = unique(points, axis=0) # Remove any duplicates
        points_of_points.append(points)

    print(len(points_of_points))

    for points in points_of_points:
        for p in points:
            id = "%.1f_%.1f" % (p[0], p[1])
            if not G.has_node(id):
                G.add_node(id, coords=p)
                #print("Node already exists.")
                #else:

        n_points_minus_one = len(points)-1
        for pidx in range(0, n_points_minus_one):
            p1 = points[pidx]
            p2 = points[pidx+1]
            u = "%.1f_%.1f" % (p1[0], p1[1])
            v = "%.1f_%.1f" % (p2[0], p2[1])
            if not G.has_node(u) or not G.has_node(v):
                print(u, v)
                print("Node issue")

            if G.has_edge(u, v):
                print("Repeated edge detected")
                print(u, v)
            else:
                G.add_edge(
                    u, v, 
                    w=None, 
                    dist=norm(p1-p2),
                    removable=False,
                    travel_move=False
                )

    ####################################

    # now going back for the 45 degree lines
    points_of_points = []
    for l1 in self.diagonal_infill_layer_lines[layer]:
        
        # Gather the intersecting points along l1's path
        points = []
        for l2 in self.vertical_infill_layer_lines[layer]:
            x, y = intersect(l1, l2)
            if x:
                points.append([round(x, 1), round(y, 1)])
        
        points = asarray(points)
        if len(points) > 0:
            for p in l1:
                if not any((points[:]==p).all(1)):
                    points = append(points, [round(p, 1)], axis=0)
        else:
            points = l1
        points = points[points[:, 0].argsort()]
        points = points[points[:, 1].argsort()]
        points = unique(points, axis=0) # Remove any duplicates
        points_of_points.append(points)

    for points in points_of_points:
        print("Processing Diagonal Points")
        for p in points:
            id = "%.1f_%.1f" % (p[0], p[1])
            if not G.has_node(id):
                G.add_node(id, coords=p)
                #print("Node already exists.")
                #else:

        n_points_minus_one = len(points)-1
        for pidx in range(0, n_points_minus_one):
            p1 = points[pidx]
            p2 = points[pidx+1]
            u = "%.1f_%.1f" % (p1[0], p1[1])
            v = "%.1f_%.1f" % (p2[0], p2[1])
            if not G.has_node(u) or not G.has_node(v):
                print(u, v)
                print("Node issue")

            if G.has_edge(u, v):
                print("Repeated edge detected")
                print(u, v)
            else:
                midpoint_x_idx = int( 
                    ( ( p1[0] - self.x_min ) / (self.x_max - self.x_min) ) * 100 
                )
                midpoint_y_idx = int( 
                    ( ( p1[1] - self.y_min ) / (self.y_max - self.y_min) ) * 100
                )
                midpoint_z_idx = int( 
                    ( (0.3 * layer ) / (self.z_max - self.z_min) ) * 100
                )
                w = self.griddata[midpoint_y_idx, midpoint_x_idx, midpoint_z_idx]
                G.add_edge(
                    u, v, 
                    w=w, 
                    dist=norm(p1-p2),
                    removable=True,
                    travel_move=False
                )

    return G