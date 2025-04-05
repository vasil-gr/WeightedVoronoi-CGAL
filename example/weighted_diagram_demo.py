import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from voronoi import weighted_voronoi as wv
from shapely.geometry import Polygon, box
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def filter_cells_outside_bbox(cells, bbox):
    """
    Returns a new list of Voronoi cells whose polygons are COMPLETELY
    contained within the bounding box [minx, maxx] x [miny, maxy].
    If a polygon goes outside the box, it is skipped and not returned.
    """
    result = []
    minx, miny, maxx, maxy = bbox
    clip_box = box(minx, miny, maxx, maxy)

    for cell in cells:
        poly_coords = cell.boundary
        if len(poly_coords) < 3:
            continue

        polygon = Polygon(poly_coords)
        if polygon.is_empty:
            continue

        # Crossing with a frame
        intersection = polygon.intersection(clip_box)
        if intersection.is_empty:
            continue
        if not intersection.equals(polygon):
            continue

        result.append(cell)

    return result


def draw_voronoi_cells(points, cells, bbox, outfile="diagram.png"):
    """
    Draws the Apollonius (weighted Voronoi) cells, assuming that cells
    have already been filtered to fit within the bounding box [minx, maxx] x [miny, maxy].
    """
    minx, miny, maxx, maxy = bbox
    plt.figure(figsize=((maxx - minx) * 1.5, (maxy - miny) * 1.5))

    # Draw bounding box
    bbox_rect = plt.Rectangle((minx, miny), maxx - minx, maxy - miny,
                              fill=False, linestyle='--', edgecolor='gray', linewidth=1)
    plt.gca().add_patch(bbox_rect)

    # Polygons
    for cell in cells:
        poly = cell.boundary
        if not poly or len(poly) < 3:
            continue

        shapely_poly = Polygon(poly)
        if shapely_poly.is_empty:
            continue

        if shapely_poly.geom_type == 'Polygon':
            xs, ys = shapely_poly.exterior.xy
            plt.plot(xs, ys, linestyle="-", color="blue")
        elif shapely_poly.geom_type == 'MultiPolygon':
            for subpoly in shapely_poly.geoms:
                xs, ys = subpoly.exterior.xy
                plt.plot(xs, ys, linestyle="-", color="blue")

    # Points
    xs_pts = [p[0] for p in points]
    ys_pts = [p[1] for p in points]
    plt.scatter(xs_pts, ys_pts, color="red", zorder=2)

    # Weight != 0
    if weights is not None and len(weights) == len(points):
        for (px, py), w in zip(points, weights):
            if abs(w) > 1e-9:
                plt.text(
                    px + 0.12,
                    py,
                    f"{w:+.2f}",
                    fontsize=6,
                    color="black",
                    ha='left',
                    va='center'
                )

    plt.axis("equal")
    plt.ylim(maxy, miny)
    plt.title("Apollonius Voronoi diagram")
    plt.savefig(outfile)
    plt.close()


if __name__ == "__main__":
    # Example
    points = [
        (1.39, 0.25), (2.75, 2.23), (1.36, 1.77), (1.92, 0.87), (0.88, 0.22),
        (0.11, 1.83), (3.35, 1.12), (1.05, 1.08), (3.33, 1.04), (3.76, 1.05),
        (1.47, 2.34), (0.01, 1.67), (2.23, 2.77), (1.65, 1.50), (1.91, 0.19),
        (0.98, 0.24), (0.28, 2.84), (2.65, 1.34), (0.45, 2.29), (3.40, 3.40),
        (2.41, 0.75), (3.00, 3.22), (2.59, 2.59), (1.18, 0.07), (1.52, 2.07)
    ]

    bbox = (0, 0, 4, 3.6)

    weights = [
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, -0.08, 0.0, 0.0,
        -0.06, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, -0.1, 0.0,
        0.0, 0.0, 0.04, 0.0, -0.06
    ]

    # Note: In general, weights should be constrained (to avoid degenerate behavior).
    # One way to do this is by estimating the average spacing between points
    # using the formula: 0.5 * sqrt(w * h / N), where w and h are the bounding box dimensions and N is the number of points.
    # For example, here: k = 0.5 * sqrt(4 * 3.5 / 28) ≈ 0.37
    # Then, we can limit the weights to the range (-a*k, +a*k),
    # where a is a user-defined coefficient (chosen experimentally).
    # Setting weight = 0 gives a standard Voronoi diagram.

    # All bounded faces
    cells = wv.build_apollonius_polygons(points, weights)
    print(f"Number of bounded faces (raw): {len(cells)}")

    # Filtering with bbox
    filtered_cells = filter_cells_outside_bbox(cells, bbox)
    print(f"Number of faces fully inside [0..4]: {len(filtered_cells)}")

    # Results
    for c in filtered_cells:
        print(f"Cell {c.index}, boundary={c.boundary}")

    draw_voronoi_cells(points, filtered_cells, bbox, outfile=os.path.join("example", "diagram.png"))
    print("Saved to diagram.png")
