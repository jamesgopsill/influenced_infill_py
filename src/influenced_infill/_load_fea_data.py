from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator

from numpy import genfromtxt, min, max, linspace, meshgrid
from scipy import interpolate

def load_fea_data(self: InfluencedInfillGenerator):
    if self.debug: print("Loading FEA data")
    fea_data = genfromtxt(self.fea_fullpath, delimiter=",")
    self.x_min = min(fea_data[:,4])
    self.x_max = max(fea_data[:,4])
    self.y_min = min(fea_data[:,5])
    self.y_max = max(fea_data[:,5])
    self.z_min = min(fea_data[:,6])
    self.z_max = max(fea_data[:,6])

    dx = linspace(self.x_min, self.x_max, 100)
    dy = linspace(self.y_min, self.y_max, 100)
    dz = linspace(self.z_min, self.z_max, 100)

    X, Y, Z = meshgrid(dx, dy, dz)
    self.griddata = interpolate.griddata(
        fea_data[:,4:7], 
        fea_data[:,7], 
        (X, Y, Z), 
        method="nearest"
    )
    if self.debug: print("FEA data loaded")