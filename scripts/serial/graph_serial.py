import matplotlib.pyplot as plt

# 8000,18.6125
# 8000,18.7467
# 8000,18.7048
# 8000,18.6971
# 12000,42.2275
# 12000,42.1712
# 12000,42.2518
# 12000,42.3559
# 14000,57.64
# 14000,58.3126
# 14000,57.5417
# 14000,57.4424
# 16000,75.3232
# 16000,76.4262
# 16000,75.8576
# 16000,75.1834
# 18000,95.5578
# 18000,96.2833
# 18000,94.7175
# 18000,94.9413


# Sample data: dictionary where keys are categories and values are lists of numbers
data = {
    '8000': [18.6125, 18.7467, 18.7048, 18.6971],
    '12000': [42.2275, 42.1712, 42.2518, 42.3559],
    '14000': [57.64, 58.3126, 57.5417, 57.4424],
    '16000': [75.3232, 76.4262, 75.8576, 75.1834],
    '18000': [95.5578, 96.2833, 94.7175, 94.9413]
}

# Calculate the average for each category
categories = list(data.keys())
averages = [sum(values) / len(values) for values in data.values()]

# Create a bar chart
plt.figure(figsize=(8, 6))
plt.bar(categories, averages, color='skyblue')

# Add labels and title
plt.xlabel('Size of Strings')
plt.ylabel('average execution time')
plt.title('Execution times for different number of strings in LCS serial implementation')

# Show the graph
plt.show()
