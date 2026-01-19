"""
The underlying functions ps_intersect (for generating the base intersecting grid structure) and Path_fill (for dense point population)
"""

def ps_intersect(primary_sf: float = 1, secondary_sf: float = 1, theta: float = 0, grid_number: int = 4, side_offset: float = 2, secondary: bool = True, centralized: bool = False, rotation_angle: float = 0):
    """
    The `ps_intersect` function (meaning primary-secondary intersect) generates an intersecting structure composed of line segments in two directions.
- The spacing between primary-direction line segments is `primary_sf`.
- The distance between adjacent intersection points of primary and secondary-direction line segments is `secondary_sf`.
- The angle between the primary direction and the horizontal direction is `rotation_angle`, while the angle between the secondary direction and the perpendicular to the primary direction is `theta` (all angles are in radians).
- `side_offset` represents the offset distance outside the grid.
- `grid_number` indicates the grid count in each direction.
- If `centralized` is `False`, the pattern starts at (0,0); if `True`, the pattern is centered at (0,0).
- Set `secondary` to `False` if secondary-direction line segments are not required.
- The function outputs two 1D NumPy arrays: `pts_x = (x1, x2, x3, ...)` and `pts_y = (y1, y2, y3, ...)`.
"""
    original_pts = np.array([0, 0]).reshape(1, 2)
    # generate the primary direction
    for i in range(int(grid_number / 2) + 1):
        x1 = 2 * i * primary_sf * tan(theta)
        y1 = 2 * i * primary_sf
        x2 = x1 + grid_number * secondary_sf + 2 * side_offset
        y2 = y1
        x3 = x2 + primary_sf * tan(theta)
        y3 = y2 + primary_sf
        x4 = x3 - grid_number * secondary_sf - 2 * side_offset
        y4 = y3
        cycle_ary = np.array([(x1, y1), (x2, y2), (x3, y3), (x4, y4)]).reshape(4, 2)
        original_pts = np.vstack((original_pts, cycle_ary))
    original_pts = original_pts[:-2, :]
    x0 = original_pts[-1, 0]
    y0 = original_pts[-1, 1]
    # generate the secondary direction
    if secondary:
        for j in range(int(grid_number / 2) + 1):
            x1 = x0 - side_offset * (1 - sin(theta)) - 2 * j * secondary_sf
            y1 = y0 + side_offset * cos(theta)
            y2 = - side_offset * cos(theta)
            x2 = x1 - (y1 - y2) * tan(theta)
            x3 = x2 - secondary_sf
            y3 = y2
            x4 = x1 - secondary_sf
            y4 = y1
            cycle_ary = np.array([(x1, y1), (x2, y2), (x3, y3), (x4, y4)]).reshape(4, 2)
            original_pts = np.vstack((original_pts, cycle_ary))
    original_pts = original_pts[1:-2, :]  # remove the first and last point
    original_pts_x = original_pts[:, 0]
    original_pts_y = original_pts[0:, 1]
    if centralized:
        x_center = side_offset + grid_number / 2 * primary_sf * tan(theta) + grid_number / 2 * secondary_sf
        y_center = grid_number / 2 * primary_sf
        original_pts_x = original_pts[:, 0] - x_center
        original_pts_y = original_pts[:, 1] - y_center
    original_pts_x, original_pts_y = original_pts_x * cos(rotation_angle) - original_pts_y * sin(rotation_angle), \
                                     original_pts_x * sin(rotation_angle) + original_pts_y * cos(rotation_angle)
    return original_pts_x, original_pts_y



#Path_fill is used to fill the path with points; the max-dis dictates the maximum distance between the adjacent points

def Path_fill(points, max_dis: float):
    def distance(p1, p2):
        return np.sqrt(np.sum((p1 - p2) ** 2))

    def interpolate(p1, p2, num_points):
        return np.linspace(p1, p2, num_points + 2)[1:-1]

    new_points = [points[0]]

    for i in range(1, len(points)):
        p1 = points[i - 1]
        p2 = points[i]
        dist = distance(p1, p2)

        if dist > max_dis:
            num_points = int(dist / max_dis)
            new_points.extend(interpolate(p1, p2, num_points))

        new_points.append(p2)

    return np.array(new_points)
