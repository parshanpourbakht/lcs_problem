import matplotlib.pyplot as plt
import numpy as np

# Size,Time (seconds)
# 8000,5.14734
# 8000,5.14426
# 8000,5.14265
# 8000,5.14174
# 8000,5.2566
# 8000,5.24145
# 8000,5.21336
# 8000,5.21254
# 8000,5.24366
# 8000,5.22196
# 8000,5.21967
# 8000,5.22467
# 8000,5.1551
# 8000,5.16247
# 8000,5.16344
# 8000,5.16667
# 12000,11.5859
# 12000,11.5893
# 12000,11.6234
# 12000,11.5931
# 12000,11.8833
# 12000,11.7664
# 12000,11.8893
# 12000,11.8838
# 12000,11.7056
# 12000,11.6788
# 12000,11.7745
# 12000,11.741
# 12000,11.7504
# 12000,11.761
# 12000,11.7429
# 12000,11.7096
# 14000,15.8481
# 14000,15.7892
# 14000,15.8266
# 14000,15.7877
# 14000,16.2008
# 14000,16.1824
# 14000,15.9605
# 14000,16.0122
# 14000,16.0583
# 14000,15.9946
# 14000,16.086
# 14000,15.9795
# 14000,16.1423
# 14000,16.0832
# 14000,16.1054
# 14000,16.1062
# 16000,20.8444
# 16000,20.8166
# 16000,20.7605
# 16000,20.7514
# 16000,21.178
# 16000,21.7856
# 16000,21.7757
# 16000,21.7962
# 16000,21.1927
# 16000,21.2235
# 16000,21.2588
# 16000,21.2967
# 16000,21.1172
# 16000,21.1407
# 16000,21.0635
# 16000,21.1496
# 18000,26.2502
# 18000,26.2802
# 18000,26.2442
# 18000,26.2443
# 18000,26.8111
# 18000,26.7445
# 18000,27.0784
# 18000,27.0776
# 18000,26.5645
# 18000,27.0572
# 18000,26.6908
# 18000,27.1525
# 18000,26.703
# 18000,26.6553
# 18000,26.646
# 18000,26.6466



# Sample data: dictionary where keys are string sizes and values are lists of execution times for each process count
data = {
    8000: {
        1: [5.14734, 5.14426, 5.14265, 5.14174],
        2: [5.2566, 5.24145, 5.21336, 5.21254],
        4: [5.24366, 5.22196, 5.21967, 5.22467],
        8: [5.1551, 5.16247, 5.16344, 5.16667],
    },
    12000: {
        1: [11.5859, 11.5893, 11.6234, 11.5931],
        2: [11.8833, 11.7664, 11.8893, 11.8838],
        4: [11.7056, 11.6788, 11.7745, 11.741],
        8: [11.7504, 11.761, 11.7429, 11.7096],
    },
    14000: {
        1: [15.8481, 15.7892, 15.8266, 15.7877],
        2: [16.2008, 16.1824, 15.9605, 16.0122],
        4: [16.0583, 15.9946, 16.086, 15.9795],
        8: [16.1423, 16.0832, 16.1054, 16.1062],
    },
    16000: {
        1: [20.8444, 20.8166, 20.7605, 20.7514],
        2: [21.178, 21.7856, 21.7757, 21.7962],
        4: [21.1927, 21.2235, 21.2588, 21.2967],
        8: [21.1172, 21.1407, 21.0635, 21.1496],
    },
    18000: {
        1: [26.2502, 26.2802, 26.2442, 26.2443],
        2: [26.8111, 26.7445, 27.0784, 27.0776],
        4: [26.5645, 27.0572, 26.6908, 27.1525],
        8: [26.703, 26.6553, 26.646, 26.6466],
    }
}

# Extract string sizes and process counts
string_sizes = list(data.keys())
process_counts = list(next(iter(data.values())).keys())

# Calculate average execution times for each string size and process count
averages = {
    process_count: [
        sum(data[size][process_count]) / len(data[size][process_count])
        for size in string_sizes
    ]
    for process_count in process_counts
}


colors = ['yellow', 'orange', 'darkgreen', 'brown']
# Plotting
x = np.arange(len(string_sizes))  # X positions for the groups
bar_width = 0.2  # Width of each bar

plt.figure(figsize=(10, 6))

for i, (process_count, color) in enumerate(zip(process_counts, colors)):
    plt.bar(
        x + i * bar_width,
        averages[process_count],
        width=bar_width,
        label=f"{process_count} Processes",
        color=color  # Custom color for this thread count
    )

# Add labels and title
plt.xlabel('Size of Strings')
plt.ylabel('Average Execution Time (s)')
plt.title('Execution Times for Different String Sizes (Distributed LCS)')
plt.xticks(x + bar_width * (len(process_counts) - 1) / 2, string_sizes)
plt.legend(title="Process Counts")

# Show the graph
plt.tight_layout()
plt.show()
