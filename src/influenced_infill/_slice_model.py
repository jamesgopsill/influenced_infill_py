from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator

import subprocess

def slice_model(self: InfluencedInfillGenerator):
    gcode_fpath = self.stl_fullpath.replace(".stl", ".gcode")
    subprocess.run([
        "slic3r", 
        "--gcode-comments", 
        self.stl_fullpath, 
        "--fill-pattern", 
        "grid", 
        "--fill-density", 
        "40", 
        "--fill-angle", 
        "0",
        "--print-center",
        "0,0"
    ])
    with open(gcode_fpath) as f:
        self.vertical_grid_gcode = f.read().replace("\r", "").split("\n")
    subprocess.run([
        "slic3r", 
        "--gcode-comments", 
        self.stl_fullpath, 
        "--fill-pattern", 
        "grid", 
        "--fill-density", 
        "56.6", 
        "--fill-angle", 
        "45",
        "--print-center",
        "0,0"
    ])
    with open(gcode_fpath) as f:
        self.diagonal_grid_gcode = f.read().replace("\r", "").split("\n")