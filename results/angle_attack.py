
porous_data = """
0                       2.83248          10
5                       2.81712          9.9619
10                      2.77696          9.8481
15                      2.71166          9.6592
20                      2.62853          9.3969
25                      2.52935          9.0631
30                      2.40984          8.6603
-10                     2.77686          9.8481
"""

grid_data = """
0                       3.09337          10
5                       3.06613          9.9619
10                      2.99136          9.8481
15                      2.87793          9.6592
20                      2.73086          9.3969
25                      2.51077          9.0631
30                      2.26719          8.6603
-10                     3.00367          9.8481
"""

# angle_attack, k, y_inlet_velocity
def parse_data(data):
    lines = data.strip().split('\n')
    return [(float(line.split()[0]), float(line.split()[1]), float(line.split()[2])) for line in lines]

import matplotlib.pyplot as plt

# Data lists
list1 = parse_data(porous_data)
list2 = parse_data(grid_data)

# Filter out data points where the first value is negative
filtered_list1 = [(x, y) for x, y, _ in list1 if x >= 0]
filtered_list2 = [(x, y) for x, y, _ in list2 if x >= 0]

# Extract x and y values
x1, y1 = zip(*filtered_list1)
x2, y2 = zip(*filtered_list2)

# Generate the 3cos(x/180*pi) line.
import numpy as np

x = np.linspace(0, 30, 100)
y = 3*np.cos(x/180*np.pi)

# Plot the data
plt.figure(figsize=(8, 5))
plt.plot(x1, y1, label='Porous mesh', marker='o')
plt.plot(x2, y2, label='Grid mesh', marker='s')
plt.plot(x, y, label='3cos(x/180*pi)', linestyle='--')

# Customize the plot
#plt.title("Second Value Over First Value")
plt.xlabel("Angle of attack")
plt.ylabel("k")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
