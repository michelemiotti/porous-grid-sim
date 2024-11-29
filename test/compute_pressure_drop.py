import sys

# Read the final time.

with open("log.simpleFoam") as f:
    data = f.readlines()

for line in data:
    if "average(inlet) of cpMean" in line:
        cp_inlet = float(line.split(" ")[-1])
    if "average(outlet) of cpMean" in line:
        cp_outlet = float(line.split(" ")[-1])

if cp_inlet is None or cp_outlet is None:
    sys.exit(1)

if abs(cp_outlet) > 1e-10:
    print("Warning: pressure coefficient at the outlet far from zero. Value: " + str(cp_outlet))

k = cp_inlet - cp_outlet
print("Pressure drop coefficient: k = " + str(k))

with open("log.pressureDrop", "w") as f:
    f.write(str(k)+"\n")