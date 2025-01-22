
porous_data = """
1                         3.68096
2                         3.22229
3                         3.05758
4                         2.97403
5                         2.92518
7.5                       2.86537
10                        2.83248
12.5                      2.81419
15                        2.80104
"""

grid_data = """
1                         3.71405
2                         3.43121
3                         3.31287
4                         3.24388
5                         3.19791
7.5                       3.13113
10                        3.09337
12.5                      3.06889
15                        3.05151
"""

# reference_velocity, k
def parse_data(data):
    lines = data.strip().split('\n')
    return [(float(line.split()[0]), float(line.split()[1])) for line in lines]


import matplotlib.pyplot as plt

# Data lists
list1 = parse_data(porous_data)
list2 = parse_data(grid_data)

# Filter out data points where the first value is negative
filtered_list1 = [(x, y) for x, y in list1 if x >= 0]
filtered_list2 = [(x, y) for x, y in list2 if x >= 0]

# Extract x and y values
x1, y1 = zip(*filtered_list1)
x2, y2 = zip(*filtered_list2)

# Plot the data
plt.figure(figsize=(8, 5))
plt.plot(x1, y1, label='Porous mesh', marker='o')
plt.plot(x2, y2, label='Grid mesh', marker='s')

# Customize the plot
#plt.title("Second Value Over First Value")
plt.xlabel("Reference velocity")
plt.ylabel("k")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
