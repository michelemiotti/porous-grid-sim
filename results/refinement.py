
porous_data = """
1                 0.00         0.01         0.03         4.0    2                160           349212     1061062     362755     2.832
1                 0.00         0.01         0.03         4.0    3                170           789739     2478207     897380     2.788
1                 0.01         0.03         0.05         4.0    3                170           2312575    6996447     2371173    2.826
1                 0.01         0.03         0.05         4.0    4                170           4112817    12936069    4727550    2.829
1                 0.00         0.50         0.50         1.0    2                170           5058560    15188992    5071984    2.870
1                 0.02         0.06         0.10         4.0    4                170           6537589    20210388    7152326    2.886
1                 0.05         0.10         0.20         4.0    4                170           12921603   39362430    13536339   2.911
2                 0.01         0.03         0.05         4.0    4                170           17689184   53347038    179680522  2.908
2                 0.01         0.03         0.05         4.0    5                170           24209662   74908127    26576614   2.978
1                 0.10         0.15         0.20         4.0    5                160       30316175   93458603    32907032   2.980
1                 0.10         0.15         0.20         4.0    5                170       30316175   93458603    32907032   2.980
1                 0.50         0.50         0.50         1.0    5                160           31040480   93341664    31261136   2.972
"""

grid_data = """
1                 0.00         0.01         0.03         4.0    2                130           357664     1083680     370176     3.090
1                 0.00         0.01         0.03         4.0    3                130           595334     1843376     662223     1.797
1                 0.01         0.03         0.05         4.0    3                130           2426016    7315904     2473184    1.879
1                 0.01         0.03         0.05         4.0    4                130           3361296    10338547    3657883    2.040
1                 0.00         0.50         0.50         1.0    2                130           5086080    15268352    5098000    3.128
1                 0.02         0.06         0.10         4.0    4                130           5956336    18122611    6251851    2.099
1                 0.05         0.10         0.20         4.0    4                130           12340336   37274611    12635851   2.099
2                 0.01         0.03         0.05         4.0    4                130           18972352   57059200    19155152   2.184
2                 0.01         0.03         0.05         4.0    5                130           22523565   68630827    23779919   2.604
1                 0.10         0.15         0.20         4.0    5                130           25954055   79005277    27292752   2.542
1                 0.50         0.50         0.50         1.0    5                130           55669699   170908775   59796337   2.705
"""

# box_3_refinement, thick_1_rel, thick_2_rel, thick_3_rel, ratio, grid_refinement, extractAngle, cells, faces, points, k
def parse_data(data):
    return [tuple(map(float, line.split()[0:])) for line in data.strip().split('\n')]

import matplotlib.pyplot as plt

# Data lists
list1 = parse_data(porous_data)
list2 = parse_data(grid_data)

print(list1)

# Filter out data points where the first value is negative
filtered_list1 = [(x, y) for _, _, _, _, _, _, _, x, _, _, y in list1]
filtered_list2 = [(x, y) for _, _, _, _, _, _, _, x, _, _, y in list2]

# Extract x and y values
x1, y1 = zip(*filtered_list1)
x2, y2 = zip(*filtered_list2)

# Generate the 3cos(x/180*pi) line.
import numpy as np

x = np.linspace(0, 30, 100)
y = 3*np.cos(x/180*np.pi)

# Plot the data
plt.figure(figsize=(8, 5))
plt.plot(x1, y1, label='Dotted mesh', marker='o')
#plt.plot(x2, y2, label='Grid mesh', marker='s')

# Customize the plot
#plt.title("Second Value Over First Value")
plt.xlabel("Number of cells")
plt.ylabel("k")
plt.legend()
plt.grid(True)

plt.ylim(2, 3.3)  # Bottom starts at 0.2, top adjusts automatically

# Show the plot
plt.savefig('plots/k-convergence.png', bbox_inches='tight')
