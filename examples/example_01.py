from influenced_infill import InfluencedInfillGenerator
import os 
from numpy import max

dir_path = os.path.dirname(os.path.realpath(__file__))
stl_fullpath = dir_path+"/data/beam.stl"
fea_fullpath = dir_path+"/data/three_point_bend_fea.csv"

iig = InfluencedInfillGenerator(
    stl_fullpath,
    fea_fullpath,
    True
)
iig.hello()
iig.slice_model()
iig.extract_infill()
iig.plot_extracted_infill_lines(10)
iig.load_fea_data()
iig.plot_fea_slice(10)
iig.generate_influenced_infill_networks(3, 15)
iig.plot_influenced_infill_network(10)
iig.plot_weighted_network(10)
threshold = max(iig.griddata) * 0.02
print("Threshold:", threshold)
iig.generate_influenced_infill(threshold)
iig.plot_influenced_infill_print_path(10)

# TODO: Replace the gcode infill with the new gcode infill and save new gcode file.