# Continuum Deformation Framework for MEW Toolpaths

This repository contains the core Python scripts for generating, deforming, and optimizing toolpaths for Melt Electrowriting (MEW) scaffolds. These scripts implement the "Continuum Deformation Framework" to create seamless biomimetic gradients.

## Overview

The workflow generates a toolpath represented by a sequence of points. It ensures high geometric fidelity during deformation while optimizing the final point count for printing efficiency.

The process consists of three main steps:
1.  **Grid Generation & Densification:** A base intersecting grid is generated and populated with high-density points (max spacing 0.01 mm) to ensure smooth transitions during deformation.
2.  **Deformation:** Mathematical transformation functions (e.g., periodic, rippled) are applied to the toolpath.
3.  **Sampling (Post-processing):** The deformed path is resampled to ensure the distance between adjacent points is at least 0.1 mm, preventing data overload on the printer controller.

## File Structure

* **`intersecting_structure_generation.py`:**
    * Contains the core functions: `ps_intersect` (generates the base grid) and `Path_fill` (densifies the points).
* **`generate_pattern.py`:**
    * The main execution script. It generates the base grid, applies the deformation formulas, visualizes the result, and exports the raw coordinate data (`original_points.txt`).
* **`generate_composite_pattern.py`:**
    * An advanced execution script for Composite Deformations. It demonstrates how to merge multiple localized deformations into a single cohesive pattern using spatial weighting (alpha blending).
* **`post_processing.py`:**
    * Reads the raw data, filters points to optimize spacing (min 0.1 mm), and exports the final coordinates (`final_points_filtered.txt`).

## Installation

1.  Clone this repository.
2.  Install the required dependencies:

```bash
pip install -r requirements.txt