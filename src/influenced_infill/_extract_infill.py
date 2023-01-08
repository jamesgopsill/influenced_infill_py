from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator
    
from re import findall
from numpy import asarray
from math import atan2, degrees

def extract_infill(self: InfluencedInfillGenerator):

    self.vertical_infill_layer_lines = []
    line = []
    lines = []
    flag = True

    for cmd in self.vertical_grid_gcode:
        if "move to next layer" in cmd:
            self.vertical_infill_layer_lines.append(lines)
            lines = []
            line = []
            continue
        if "; move to first infill point" in cmd:
            pos = findall("X([-\d.]+)\sY([-\d.]+)", cmd)
            line = [[float(pos[0][0]), float(pos[0][1])]]
            flag = True
            continue
        if cmd.endswith("; infill"):
            pos = findall("X([-\d.]+)\sY([-\d.]+)", cmd)
            line.append([float(pos[0][0]), float(pos[0][1])])
            if len(line) > 2:
                line.pop(0)
            if len(line) == 2 and flag == True:
                lines.append(asarray(line))
                flag = False
                continue
            if len(line) == 2 and flag != True:
                flag = True
                continue
            continue

    self.vertical_infill_layer_lines.pop(0)

    ##################

    self.diagonal_infill_layer_lines = []

    line = []
    lines = []

    for cmd in self.diagonal_grid_gcode:
        if "move to next layer" in cmd:
            self.diagonal_infill_layer_lines.append(lines)
            lines = []
            line = []
            continue
        if "; move to first infill point" in cmd:
            pos = findall("X([-\d.]+)\sY([-\d.]+)", cmd)
            line = [[float(pos[0][0]), float(pos[0][1])]]
            continue
        if cmd.endswith("; infill"):
            pos = findall("X([-\d.]+)\sY([-\d.]+)", cmd)
            line.append([float(pos[0][0]), float(pos[0][1])])
            if len(line) > 2:
                line.pop(0)
            if len(line) == 2:
                rads = atan2(line[0][1]-line[1][1], line[0][0]-line[1][0], )
                degs = degrees(rads)
                mod_45 = abs(degs) % 45
                mod_90 = abs(degs) % 90
                if mod_45 < 0.2 and mod_90 > 0.2:
                    lines.append(asarray(line))
                elif mod_45 < 45 and mod_45 > 44.98:
                    lines.append(asarray(line))
            continue

    self.diagonal_infill_layer_lines.pop(0)