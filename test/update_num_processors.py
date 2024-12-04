# A script to update the number of processors in each direction.
# It updates "decomposeOptions" and "Allrun_cluster".

import argparse
import subprocess
import sys

# Parse the inputs.
parser = argparse.ArgumentParser()
parser.add_argument("-x", type=int, help="Number of processors in the x direction")
parser.add_argument("-y", type=int, help="Number of processors in the y direction")
parser.add_argument("-z", type=int, help="Number of processors in the z direction")
args = parser.parse_args()


# Check the inputs.
if args.x is None and args.y is None and args.z is None:
    # If no arguments are given, read the old settings.
    num_processors = int(
        subprocess.check_output(["python3", "extract_num_processors.py"])
    )
    new_settings = False
elif args.x is None or args.y is None or args.z is None:
    print(
        "Error! You must either specify the number of processors in each direction or in none."
    )
    sys.exit(1)
elif args.x < 1 or args.y < 1 or args.z < 1:
    print("Error! There must be at least one processor in each direction.")
    sys.exit(1)
else:
    num_processors = args.x * args.y * args.z
    new_settings = True


# Update the cluster file.
with open("Allrun_cluster", "r") as f:
    data = f.readlines()

found_first = False
found_second = False
for idx, line in enumerate(data):
    if line.startswith("#$ -pe mpi"):
        if found_first:
            print("Error in Allrun_cluster format. Halting.")
            sys.exit(1)
        data[idx] = "#$ -pe mpi " + str(num_processors) + "           # cpuNumber\n"
        found_first = True
    if line.startswith("NUM_PROCESSORS="):
        if found_second:
            print("Error in Allrun_cluster format. Halting.")
            sys.exit(1)
        data[idx] = "NUM_PROCESSORS=" + str(num_processors) + "\n"
        found_second = True

if not found_first or not found_second:
    print("Error in Allrun_cluster format. Halting.")
    sys.exit(1)

with open("Allrun_cluster", "w") as f:
    f.writelines(data)


# Update the OpenFOAM configuration file.
if not new_settings:
    sys.exit(0)

with open("system/include/decomposeOptions", "r") as f:
    data = f.readlines()

found_x = False
found_y = False
found_z = False
for idx, line in enumerate(data):
    if line.startswith("num_x_subdomains"):
        if found_x:
            print("Error in decomposeOptions format. Halting.")
            sys.exit(1)
        data[idx] = "num_x_subdomains " + str(args.x) + ";\n"
        found_x = True
    if line.startswith("num_y_subdomains"):
        if found_y:
            print("Error in decomposeOptions format. Halting.")
            sys.exit(1)
        data[idx] = "num_y_subdomains " + str(args.y) + ";\n"
        found_y = True
    if line.startswith("num_z_subdomains"):
        if found_z:
            print("Error in decomposeOptions format. Halting.")
            sys.exit(1)
        data[idx] = "num_z_subdomains " + str(args.z) + ";\n"
        found_z = True

if not found_x or not found_y or not found_z:
    print("Error in decomposeOptions format. Halting.")
    sys.exit(1)

with open("system/include/decomposeOptions", "w") as f:
    f.writelines(data)
