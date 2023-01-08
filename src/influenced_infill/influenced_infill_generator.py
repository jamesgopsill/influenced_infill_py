from typing import List

class InfluencedInfillGenerator:

    stl_fullpath: str = ""
    fea_fullpath: str = ""
    vertical_grid_gcode: List[str] = []
    diagonal_grid_gcode: List[str] = []
    x_min: float = 0
    x_max: float = 0
    y_min: float = 0
    y_max: float = 0
    z_min: float = 0
    z_max: float = 0
    griddata: any
    vertical_infill_layer_lines: List[str] = []
    diagonal_infill_layer_lines: List[str] = []
    infill_influenced_networks: List[any] = []

    def __init__(self, 
            stl_fullpath: str, 
            fea_fullpath: str, 
            debug: bool = False
        ) -> None:
        self.debug = debug
        self.stl_fullpath = stl_fullpath
        self.fea_fullpath = fea_fullpath

    from ._hello import hello
    from ._slice_model import slice_model
    from ._load_fea_data import load_fea_data
    from ._extract_infill import extract_infill
    from ._plot_extracted_infill_lines import plot_extracted_infill_lines
    from ._generate_influenced_infill_networks import generate_influenced_infill_networks, generate_influenced_infill_network
    from ._plot_influenced_infill_network import plot_influenced_infill_network
    from ._plot_fea_slice import plot_fea_slice
    from ._plot_weighted_network import plot_weighted_network
    from ._generate_influenced_infill import generate_influenced_infill
    from ._plot_influenced_infill_print_path import plot_influenced_infill_print_path