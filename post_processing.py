"""
Post-processing script: Density-tuned point cloud
Reads a previously exported point list, removes closely-spaced
points, and exports the filtered toolpath for printing.
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# 1. Read text file
# ----------------------------------------------------------
points = []
try:
    with open("original_points.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("(") and line.endswith(")"):
                try:
                    x_str, y_str = line[1:-1].split(',')
                    points.append((float(x_str), float(y_str)))
                except ValueError:
                    print(f"Parsing error: {line}")
                    continue
except FileNotFoundError:
    print("File 'original_points.txt' not found. Please check the path.")
    exit()

# Convert list to NumPy arrays
pts_x, pts_y = zip(*points)
pts_x, pts_y = np.array(pts_x), np.array(pts_y)

# ----------------------------------------------------------
# 2. Remove points that are closer than min_distance
# ----------------------------------------------------------
def remove_close_points(points, min_distance=0.1):
    """
    Iteratively filters the point list so that consecutive points
    are separated by at least min_distance.
    """
    filtered = [points[0]]  # keep the first point
    for curr in points[1:]:
        last = filtered[-1]
        if np.linalg.norm(np.array(curr) - np.array(last)) >= min_distance:
            filtered.append(curr)
    return filtered

filtered_pts = remove_close_points(points, min_distance=0.1)

# ----------------------------------------------------------
# 3. Visualize original vs. filtered point clouds
# ----------------------------------------------------------
plt.figure(figsize=(12, 6))

# Original data
plt.subplot(1, 2, 1)
plt.scatter(pts_x, pts_y, s=1, color='blue', label='Original')
plt.title("Original Points")
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.axis('equal')
plt.legend()

# Filtered data
filtered_pts_x, filtered_pts_y = zip(*filtered_pts)
plt.subplot(1, 2, 2)
plt.scatter(filtered_pts_x, filtered_pts_y, s=1, color='red', label='Filtered')
plt.title("Filtered Points")
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.axis('equal')
plt.legend()

plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# 4. Export filtered point list for printing
# ----------------------------------------------------------
output_file = "final_points_filtered.txt"
with open(output_file, "w") as f:
    for x, y in filtered_pts:
        f.write(f"({x:.4f}, {y:.4f})\n")

print(f"Filtered point list saved to {output_file}")