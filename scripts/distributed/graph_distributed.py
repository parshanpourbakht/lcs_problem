import matplotlib.pyplot as plt
import numpy as np

# Size,Time (seconds)
# 8000,5.1359
# 8000,5.13967
# 8000,5.12506
# 8000,5.12872
# 8000,5.33324
# 8000,5.33133
# 8000,5.32197
# 8000,5.18433
# 8000,5.17803
# 8000,5.17514
# 8000,5.17202
# 8000,5.17147
# 8000,5.18897
# 8000,5.19162
# 8000,5.19574
# 8000,5.1915
# 12000,11.6726
# 12000,11.6523
# 12000,11.6519
# 12000,11.653
# 12000,12.1485
# 12000,12.1376
# 12000,12.1318
# 12000,11.7519
# 12000,11.7683
# 12000,11.7281
# 12000,11.7528
# 12000,11.7636
# 12000,11.7955
# 12000,11.7801
# 12000,11.8126
# 12000,11.8018
# 14000,15.9664
# 14000,15.8973
# 14000,15.9262
# 14000,15.9161
# 14000,16.5969
# 14000,16.6068
# 14000,16.5874
# 14000,16.0656
# 14000,16.0596
# 14000,16.0536
# 14000,16.044
# 14000,16.0397
# 14000,16.0903
# 14000,16.0998
# 14000,16.1134
# 14000,16.1006
# 16000,20.8776
# 16000,20.8229
# 16000,20.8333
# 16000,20.8486
# 16000,21.0604
# 16000,21.3406
# 16000,21.3191
# 16000,21.1343
# 16000,21.0519
# 16000,21.0496
# 16000,21.0536
# 16000,21.0461
# 16000,21.1166
# 16000,21.1164
# 16000,21.1135
# 16000,21.0755
# 18000,26.4968
# 18000,26.4622
# 18000,26.4537
# 18000,26.4468
# 18000,27.5504
# 18000,27.5277
# 18000,27.5932
# 18000,26.9145
# 18000,26.5412
# 18000,26.5649
# 18000,26.6246
# 18000,26.6164
# 18000,27.0633
# 18000,26.9994
# 18000,27.0212
# 18000,26.9876



# Sample data: dictionary where keys are string sizes and values are lists of execution times for each process count
data = {
    8000: {
        1: [5.1359, 5.13967, 5.12506, 5.12872],
        2: [5.33324, 5.33133, 5.32197, 5.18433],
        4: [5.17803, 5.17514, 5.17202, 5.17147],
        8: [5.18897, 5.19162, 5.19574, 5.1915],
    },
    12000: {
        1: [11.6726, 11.6523, 11.6519, 11.653],
        2: [12.1485, 12.1376, 12.1318, 11.7519],
        4: [11.7683, 11.7281, 11.7528, 11.7636],
        8: [11.7955, 11.7801, 11.8126, 11.8018],
    },
    14000: {
        1: [15.9664, 15.8973, 15.9262, 15.9161],
        2: [16.5969, 16.6068, 16.5874, 16.0656],
        4: [16.0596, 16.0536, 16.044, 16.0397],
        8: [16.0903, 16.0998, 16.1134, 16.1006],
    },
    16000: {
        1: [20.8776, 20.8229, 20.8333, 20.8486],
        2: [21.0604, 21.3406, 21.3191, 21.1343],
        4: [21.0519, 21.0496, 21.0536, 21.0461],
        8: [21.1166, 21.1164, 21.1135, 21.0755],
    },
    18000: {
        1: [26.4968, 26.4622, 26.4537, 26.4468],
        2: [27.5504, 27.5277, 27.5932, 26.9145],
        4: [26.5412, 26.5649, 26.6246, 26.6164],
        8: [27.0633, 26.9994, 27.0212, 26.9876],
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
