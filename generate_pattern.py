"""
Generates a periodic pattern from an intersecting base grid,
applies periodic deformation, and exports the printing toolpath.
"""

from intersecting_structure_generation import (
    ps_intersect,
    Path_fill
)
from math import pi, sqrt, exp, atan2
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# 1. Geometry & grid parameters
# -----------------------------------------------------------
primary_sf   = 0.5      # primary scaling factor for the base grid
secondary_sf = 0.5      # secondary scaling factor
side_offset  = 1        # offset distance
theta        = 0        # skew angle between intersecting lines (must not be an odd multiple of π/2)
grid_number  = 40       # number of grid numbers along each direction
rotation_angle = 0      # global rotation of the pattern (radians)

# Generate the base intersecting grid
pts_x_single, pts_y_single = ps_intersect(
    primary_sf=primary_sf,
    secondary_sf=secondary_sf,
    side_offset=side_offset,
    theta=theta,
    grid_number=grid_number,
    rotation_angle=rotation_angle,
    centralized=True
)

# -----------------------------------------------------------
# 2. Path refinement
# -----------------------------------------------------------
pts = np.column_stack((pts_x_single, pts_y_single))  # (N,2) array
# Dense filling points
pts = Path_fill(points=pts, max_dis=0.01)
pts_x_single, pts_y_single = zip(*pts)
pts_x_single = np.array(pts_x_single)
pts_y_single = np.array(pts_y_single)

# -----------------------------------------------------------
# 3. Apply periodic deformation
#    Modify the equations below to explore other patterns
# -----------------------------------------------------------
# Periodic-1
pts_x = np.sin(pts_x_single) + 2 * pts_x_single + 0.5 * pts_y_single
pts_y = np.sin(pts_y_single) + 2 * pts_y_single + 0.5 * pts_x_single

# Periodic-2
# pts_x = np.sin(pts_x_single) * np.sin(pts_y_single) + 2 * pts_x_single
# pts_y = np.cos(pts_x_single) * np.cos(pts_y_single) + 2 * pts_y_single

# -----------------------------------------------------------
# 4. Post-processing: scaling & translation
# -----------------------------------------------------------
scale_factor = 0.5              # overall size reduction
translation_x = 20              # horizontal shift (mm)
translation_y = 20              # vertical shift   (mm)

pts_x = pts_x * scale_factor + translation_x
pts_y = pts_y * scale_factor + translation_y

# -----------------------------------------------------------
# 5. Visualization & export
# -----------------------------------------------------------
plt.plot(pts_x, pts_y, color='black', linewidth=1)
plt.axis('equal')
plt.axis('off')
plt.savefig('periodic_pattern.png', dpi=900)
plt.show()

# Export final coordinates for printing
output_file = "original_points.txt"
with open(output_file, "w") as f:
    for x, y in zip(pts_x, pts_y):
        f.write(f"({x:.4f}, {y:.4f})\n")