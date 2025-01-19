import sys
import os
# Create and apply a mesh with the provided options.
# This script modifies domain geometry, but not refinement,
# which should be changed in the appropriate OpenFOAM dictionaries.
# Make sure to run this script inside "simulation" and to have
# the environmental variable "BLENDER_PATH" set correctly.

""" ----------------- EDITABLE SETTINGS ----------------- """
# Choose the mesh. The options are "porous", "grid".
mesh = "grid"

# Options for porous mesh (in meters).
# Meaning explained in README.md.
cavity_diameter = 2 / 100
cavity_distancing = 0.5 / 100
slate_thickness = 2.5 / 100

# Options for grid mesh (in meters).
# Meaning explained in README.md.
square_size = 2.5 / 100
overlap_offset = 0.6 / 100
bevel_resolution = 10
wire_section_radius = 0.5 / 100

# Options for the domain.
length = 1.0  # Length of the domain in meters.
num_copies = 2  # Number of copies of the grid before periodicity is applied.
# Note that for the "grid" mesh, this is half the number of squares.
""" ----------------- EDITABLE SETTINGS ----------------- """


# Compute the derived parameters.
if mesh == "porous":
    domain_length = cavity_diameter + cavity_distancing
    base = domain_length * num_copies
    cavity_amount = num_copies + 2
    if slate_thickness > length:
        print("Error! Wrong parameters for porous mesh.")
        sys.exit(1)
    y_in_fluid = length / 2 - 1e-6
else:
    if mesh != "grid":
        print("Error! Selected an invalid grid type.")
        sys.exit(1)
    domain_length = square_size * 2
    base = domain_length * num_copies
    square_amount = 2 * num_copies + 2
    if overlap_offset + wire_section_radius > length / 2:
        print("Error! Wrong parameters for grid mesh.")
        sys.exit(1)
    y_in_fluid = length / 2 - 1e-6


# Create the desired mesh.
filename = "constant/triSurface/grid.obj"
if mesh == "porous":
    os.system(
        f"$BLENDER_PATH --background --python ../mesh-generators/generate_porous_mesh.py -- \
               --export_path {filename}                \
               --cavity_amount {cavity_amount}         \
               --cavity_diameter {cavity_diameter}     \
               --cavity_distancing {cavity_distancing} \
               --slate_thickness {slate_thickness}"
    )
else:
    os.system(
        f"$BLENDER_PATH --background --python ../mesh-generators/generate_wire_mesh.py -- \
               --export_path {filename}                \
               --square_size {square_size}             \
               --square_amount {square_amount}         \
               --overlap_offset {overlap_offset}       \
               --bevel_resolution {bevel_resolution}   \
               --wire_section_radius {wire_section_radius}"
    )


# Update domain parameters.
with open("system/include/meshParameters", "r") as f:
    data = f.readlines()

base_found = False
length_found = False
y_in_fluid_found = False

for idx, line in enumerate(data):
    if line.startswith("base"):
        if base_found:
            print("Error! meshParameters file does not have the expected format.")
            sys.exit(1)
        data[idx] = "base " + str(base) + ";\n"
        base_found = True
    if line.startswith("length"):
        if length_found:
            print("Error! meshParameters file does not have the expected format.")
            sys.exit(1)
        data[idx] = "length " + str(length) + ";\n"
        length_found = True
    if line.startswith("y_in_fluid"):
        if y_in_fluid_found:
            print("Error! meshParameters file does not have the expected format.")
            sys.exit(1)
        data[idx] = "y_in_fluid " + str(y_in_fluid) + ";\n"
        y_in_fluid_found = True

if not base_found or not length_found or not y_in_fluid_found:
    print("Error! meshParameters file does not have the expected format.")
    sys.exit(1)

with open("system/include/meshParameters", "w") as f:
    f.writelines(data)
