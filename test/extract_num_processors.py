# Read and return the number of subdomains.
# Note: the script fails if it returns any number lower than 1, including 0.

import sys

with open("system/include/decomposeOptions") as f:
    data = f.readlines()


num_x_subdomains = -1
num_y_subdomains = -1
num_z_subdomains = -1

for line in data:
    if "num_x_subdomains" in line:
        num_x_subdomains = int(line.split(" ")[1].split(";")[0])
    if "num_y_subdomains" in line:
        num_y_subdomains = int(line.split(" ")[1].split(";")[0])
    if "num_z_subdomains" in line:
        num_z_subdomains = int(line.split(" ")[1].split(";")[0])

if num_x_subdomains < 1 or num_y_subdomains < 1 or num_z_subdomains < 1:
    sys.exit(-1)

num_subdomains = num_x_subdomains * num_y_subdomains * num_z_subdomains

print(num_subdomains)