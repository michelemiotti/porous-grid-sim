
data = """6      62.11            86.35
5      78.47            95.91
4      72.27            112.53
3      103.73           132.82
2      134.68           177.08
1      249.77           295.52"""

# returns list of correctly-sized tuples
def parse_data(data):
    return [tuple(map(float, line.split()[0:])) for line in data.strip().split('\n')]


import matplotlib.pyplot as plt

list1 = parse_data(data)

filtered_list1 = [(x, y) for x, y, _ in list1]
filtered_list2 = [(x, y) for x, _, y in list1]

# Extract x and y values
x1, y1 = zip(*filtered_list1)
x2, y2 = zip(*filtered_list2)


# Generate the 250/x line with 200 samples.
x = [x/200 + 1 for x in range(1, 200*5+1)]
y = [250 / i for i in x]


# Plot the data
plt.figure(figsize=(8, 5))
plt.plot(x1, y1, label='snappyHexMesh time', marker='o')
plt.plot(x2, y2, label='simpleFoam time', marker='o')
plt.plot(x, y, label='Ideal scaling', linestyle='--')

# Customize the plot
#plt.title("Second Value Over First Value")
plt.xlabel("Core count")
plt.ylabel("Time (s)")
plt.legend()
plt.grid(True)

# Show the plot
plt.savefig('plots/core-scaling.png', bbox_inches='tight')
