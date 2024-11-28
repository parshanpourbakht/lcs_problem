import matplotlib.pyplot as plt

#8000, 12000, 14000, 16000, 18000

# Sample data: dictionary where keys are categories and values are lists of numbers
data = {
    '8000': [18.662, 18.6344, 18.6533, 18.6037],
    '12000': [42.4051, 42.0451, 42.1263, 41.9899],
    '14000': [57.3757, 57.5254, 57.2519, 57.7335],
    '16000': [74.9689, 75.4585, 75.0174, 75.4856],
    '18000': [95.6915, 94.5645, 94.4948, 95.5719]
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
