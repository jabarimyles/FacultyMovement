import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Define the sample size and categories
n_samples = 311
categories = ['N.America', 'Europe', 'Asia', 'Australia', 'Crosscultural', 'L.America', 'Africa', 'Oceania']
category_sizes = [80, 65, 55, 30, 25, 20, 15, 21]  # Sizes of each category
category_colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3']

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 5))

# Create grid of people (icons)
x_positions = np.arange(0, 11)  # 11 people per row
y_positions = np.arange(0, n_samples // len(x_positions) + 1)  # enough rows to hold all samples

# Flatten the x and y positions for each person
x = np.tile(x_positions, len(y_positions))
y = np.repeat(y_positions, len(x_positions))

# Now we assign each person to a category
category_boundaries = np.cumsum(category_sizes)
category_indices = np.hstack([np.repeat(i, size) for i, size in enumerate(category_sizes)])

# Plot each "person" (icon)
for i in range(n_samples):
    ax.scatter(x[i], y[i], color=category_colors[category_indices[i]], s=300, marker='o')

# Add legend
patches = [mpatches.Patch(color=category_colors[i], label=categories[i]) for i in range(len(categories))]
ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

# Adjust the axis limits
ax.set_xlim(-0.5, max(x_positions) + 0.5)
ax.set_ylim(-0.5, len(y_positions))

# Remove axes and labels
ax.axis('off')

# Add title and subtitle
plt.title('Samples (N=311)', fontsize=16, loc='left')
plt.text(-0.5, len(y_positions) + 0.5, '1 human = 1 sample', fontsize=10, verticalalignment='center')

# Show plot
plt.tight_layout()
plt.savefig('viz.png')
