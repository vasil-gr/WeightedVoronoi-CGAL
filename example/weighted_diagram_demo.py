from voronoi import weighted_voronoi as wv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt



def draw_voronoi_cells(points, cells, outfile="diagram.png"):
    """
    Draws the Apollonius (weighted Voronoi) cells, assuming that cells
    have already been filtered to fit within the bounding box [minx, maxx] x [miny, maxy].
    """
    plt.figure()

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
                    px - 0.05,
                    py,
                    f"{w:.2f}",
                    fontsize=6,
                    color="black",
                    ha='right',
                    va='center'
                )

    plt.xlim(0, 4)
    plt.ylim(4, 0)
    plt.axis("equal")
    plt.title("Apollonius Weighted Voronoi")
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
    weights = [
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0
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

    # Results
    for c in cells:
        print(f"Cell {c.index}, boundary={c.boundary}")

    draw_voronoi_cells(points, cells, "diagram.png")
    print("Saved to diagram.png")
