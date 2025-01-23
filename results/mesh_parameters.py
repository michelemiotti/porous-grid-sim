

big_data = [
    """2                     0.5                     0.625                     2.76027
2                     0.5                     1.25                      2.84406
2                     0.5                     2.5                       2.83248
2                     0.5                     5                         2.91072
2                     0.5                     7.5                       3.0048
2                     0.5                     10                        3.12328""",



"""1.25                  1.25                    2.5                       34.7274       0.5                                   0.196350
1.5                   1                       2.5                       14.4402       0.6                                   0.282743
1.75                  0.75                    2.5                       6.32234       0.7                                   0.384845
2                     0.5                     2.5                       2.83248       0.8                                   0.502654
2.25                  0.25                    2.5                       1.18552       0.9                                   0.636172
2.4                   0.1                     2.5                       0.626318      0.96                                  0.723823
2.475                 0.025                   2.5                       0.43754       0.99   0""",



"""2.5                   0.6                     0.125                     0.206435
2.5                   0.6                     0.25                      0.497481
2.5                   0.6                     0.4                       1.01028
2.5                   0.6                     0.45                      1.18621
2.5                   0.6                     0.5                       3.09337
2.5                   0.6                     0.55                      3.60406
2.5                   0.6                     0.6                       3.68879""",



"""2.5                   0.5                     0.5                       3.56465
2.5                   0.55                    0.5                       3.57318
2.5                   0.6                     0.5                       3.09337
2.5                   0.65                    0.5                       2.81168
2.5                   0.7                     0.5                       2.59965"""

]

# returns list of correctly-sized tuples
def parse_data(data):
    return [tuple(map(float, line.split()[0:])) for line in data.strip().split('\n')]


import matplotlib.pyplot as plt


for TARGET_DATA in (0, 1, 2, 3):
    data = big_data[TARGET_DATA]

    list1 = parse_data(data)

    # Filter out data points where the first value is negative
    if TARGET_DATA == 0:
        filtered_list1 = [(x, y) for _, _, x, y in list1]
    elif TARGET_DATA == 1:
        filtered_list1 = [(x, y) for _, _, _, y, x, _ in list1]
    elif TARGET_DATA == 2:
        filtered_list1 = [(x, y) for _, _, x, y in list1]
    elif TARGET_DATA == 3:
        filtered_list1 = [(x, y) for _, x, _, y in list1]
    else:
        raise Exception("Invalid TARGET_DATA")

    # Extract x and y values
    x1, y1 = zip(*filtered_list1)

    # Generate the 3cos(x/180*pi) line.
    import numpy as np


    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(x1, y1, marker='o') #label='Porous mesh'

    # Customize the plot
    #plt.title("Second Value Over First Value")
    plt.xlabel([
        "slate_thickness (cm)",
        "r",
        "wire_section_radius (cm)",
        "overlap_offset (cm)"

    ][TARGET_DATA])
    plt.ylabel("k")
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.savefig(f'plots/{["slate_thickness", "hole_diameter", "wire_section_radius", "overlap_offset"][TARGET_DATA]}.png', bbox_inches='tight')
