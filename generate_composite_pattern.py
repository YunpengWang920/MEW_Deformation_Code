"""
Code S4
Generates a composite pattern with multiple localized deformations (Flower Swirl, Heart Wave, Hexagon Perturbation, Rose Boundary) and exports the printing toolpath.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path

# ===========================================================
# 0. Grid Initialization
# ===========================================================
n = 300
x_vals = np.linspace(-50, 50, n)
y_vals = np.linspace(-35, 50, n)
X, Y = np.meshgrid(x_vals, y_vals, indexing='xy')  # Generate grid coordinates

# Flatten to 1D arrays for processing
pts_x = X.flatten()
pts_y = Y.flatten()

# ===========================================================
# 1. Flower Swirl Deformation (Adjustable Center)
# ===========================================================
swirl_cx, swirl_cy = 0, 25  # Center of the swirl

# Local coordinate transformation
Xs = pts_x - swirl_cx
Ys = pts_y - swirl_cy
r_swirl = np.sqrt(Xs**2 + Ys**2)
theta_swirl = np.arctan2(Ys, Xs)

# Define flower shape (6 petals)
flower_shape = 0.5 + 0.5 * np.cos(6 * theta_swirl)
r1 = 4 + 4 * flower_shape  # Inner boundary
r2 = r1 + 20               # Outer boundary

# Calculate alpha weights (for blending deformation)
alpha_swirl = np.zeros_like(r_swirl)
mask_in = (r_swirl <= r1)
mask_out = (r_swirl >= r2)
alpha_swirl[mask_in] = 1
mid = ~mask_in & ~mask_out  # Transition zone
alpha_swirl[mid] = 0.5 * (1 + np.cos(np.pi * (r_swirl[mid]-r1[mid]) / (r2[mid]-r1[mid])))

# Apply swirl deformation parameters
A_swirl, B_swirl = 0.8, 0.12
C_swirl, D_swirl = 1.2, 0.4
r_swirl_prime = r_swirl * (1 + A_swirl * alpha_swirl * np.exp(-B_swirl * r_swirl))
theta_swirl_prime = theta_swirl + C_swirl * alpha_swirl * np.exp(-D_swirl * r_swirl)

# Convert back to Cartesian coordinates
x_swirl = r_swirl_prime * np.cos(theta_swirl_prime) + swirl_cx
y_swirl = r_swirl_prime * np.sin(theta_swirl_prime) + swirl_cy

# ===========================================================
# 2. Classic Heart Shape + Wave Deformation
# ===========================================================
heart_cx, heart_cy = 0, -10  # Heart center
heart_size = 0.5

# Generate heart shape parametric equation
t = np.linspace(0, 2*np.pi, 1000)
heart_x_param = 16 * (np.sin(t))**3
heart_y_param = 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)
heart_x_param = heart_size * heart_x_param + heart_cx  # Translation
heart_y_param = heart_size * heart_y_param + heart_cy

# Create heart polygon Path object
heart_poly = np.column_stack((heart_x_param, heart_y_param))
heart_path = Path(heart_poly, closed=True)
in_heart = heart_path.contains_points(np.column_stack((X.flatten(), Y.flatten()))).reshape(X.shape)

# Calculate distance to the boundary
dists = np.full(pts_x.shape, np.inf)
for i in range(len(heart_poly)-1):
    p1 = heart_poly[i]
    p2 = heart_poly[i+1]
    vec = p2 - p1
    vec_norm = np.dot(vec, vec)
    w = np.column_stack((pts_x - p1[0], pts_y - p1[1]))
    proj = np.clip(np.dot(w, vec) / vec_norm, 0, 1)
    closest = p1 + proj[:, None] * vec
    d = np.linalg.norm(np.column_stack((pts_x, pts_y)) - closest, axis=1)
    dists = np.minimum(dists, d)

# Calculate alpha weights for the heart region
D = 10  # Transition distance
raw_mask = in_heart.flatten()
alpha_heart = np.zeros_like(raw_mask, dtype=float)
alpha_heart[raw_mask] = 1.0
transition_zone = (dists <= D) & ~raw_mask
alpha_heart[transition_zone] = 0.5 * (1 + np.cos(np.pi * dists[transition_zone] / D))

# Wave deformation parameters
A_wave, B_wave = 0.3, 1.1
C_wave, D_wave = 0.3, 1.1
x_wave = A_wave * np.sin(X) * np.cos(Y) + B_wave * X
y_wave = C_wave * np.cos(X) * np.sin(Y) + D_wave * Y
x_wave_1d = x_wave.flatten()
y_wave_1d = y_wave.flatten()

# ===========================================================
# 3. Hexagon Angular Perturbation
# ===========================================================
hex_cx, hex_cy = -30, 7.5  # Hexagon center
X_hex = pts_x - hex_cx
Y_hex = pts_y - hex_cy
r_hex = np.sqrt(X_hex**2 + Y_hex**2)
theta_hex = np.arctan2(Y_hex, X_hex)

angle_hex = np.abs(np.mod(theta_hex, np.pi/3) - np.pi/6)
hex_radius = 12 / np.cos(angle_hex)
r1_hex = hex_radius * 0.6
r2_hex = r1_hex + 12

# Calculate alpha weights for hexagon
alpha_hex = np.zeros_like(r_hex)
in_hex = (r_hex <= r1_hex)
out_hex = (r_hex >= r2_hex)
mid_hex = ~in_hex & ~out_hex
alpha_hex[in_hex] = 1.0
alpha_hex[mid_hex] = 0.5 * (1 + np.cos(np.pi * (r_hex[mid_hex]-r1_hex[mid_hex])) / (r2_hex[mid_hex]-r1_hex[mid_hex]))

# Apply hexagon perturbation
A_hex = 0.15
k_hex = 6
r_hex_prime = r_hex * (1 + alpha_hex * A_hex * np.cos(k_hex * theta_hex))
x_hex = r_hex_prime * np.cos(theta_hex) + hex_cx
y_hex = r_hex_prime * np.sin(theta_hex) + hex_cy

# ===========================================================
# 4. Rose Boundary Perturbation
# ===========================================================
rose_cx, rose_cy = 30, 7.5  # Rose center
X_rose = pts_x - rose_cx
Y_rose = pts_y - rose_cy
r_rose = np.sqrt(X_rose**2 + Y_rose**2)
theta_rose = np.arctan2(Y_rose, X_rose)

k_flower = 6
flower_radius = 15 * (1 + 0.4 * np.cos(k_flower * theta_rose))
r1_rose = flower_radius * 0.5
r2_rose = r1_rose + 10

# Calculate alpha weights for rose
alpha_rose = np.zeros_like(r_rose)
in_rose = (r_rose <= r1_rose)
out_rose = (r_rose >= r2_rose)
mid_rose = ~in_rose & ~out_rose
alpha_rose[in_rose] = 1.0
alpha_rose[mid_rose] = 0.5 * (1 + np.cos(np.pi * (r_rose[mid_rose]-r1_rose[mid_rose]) / (r2_rose[mid_rose]-r1_rose[mid_rose])))

# Apply rose perturbation
A_rose = 0.015
k_rose = 3
r_rose_prime = r_rose * (1 + alpha_rose * A_rose * np.cos(k_rose * r_rose))
x_rose = r_rose_prime * np.cos(theta_rose) + rose_cx
y_rose = r_rose_prime * np.sin(theta_rose) + rose_cy

# ===========================================================
# 5. Composite Deformation (Merging)
# ===========================================================
x_final = (
    pts_x
    + alpha_swirl * (x_swirl - pts_x)
    + alpha_heart * (x_wave_1d - pts_x)
    + alpha_hex * (x_hex - pts_x)
    + alpha_rose * (x_rose - pts_x)
)

y_final = (
    pts_y
    + alpha_swirl * (y_swirl - pts_y)
    + alpha_heart * (y_wave_1d - pts_y)
    + alpha_hex * (y_hex - pts_y)
    + alpha_rose * (y_rose - pts_y)
)

# Reshape to grid for potential surface plotting (optional)
FinalX = x_final.reshape(n, n)
FinalY = y_final.reshape(n, n)

# ===========================================================
# 6. Visualization & Export
# ===========================================================
# Scale adjustment
scale_factor = 0.2 # Scaling factor, adjustable as needed
pts_x = x_final * scale_factor
pts_y = y_final * scale_factor

# Global translation adjustment
translation_x = 30 # X-axis translation
translation_y = 30 # Y-axis translation
pts_x = pts_x + translation_x
pts_y = pts_y + translation_y

# Plot the deformed grid
plt.scatter(pts_x, pts_y, s=1, color='blue')
plt.axis('equal')
plt.show()

# Export final point coordinates to file
output_file = "composite_points.txt"
with open(output_file, "w") as f:
    for x, y in zip(pts_x, pts_y):
        f.write(f"({x:.4f}, {y:.4f})\n")