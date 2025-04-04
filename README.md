# Apollonius Weighted Voronoi

**Apollonius (additively weighted) Voronoi diagram** with bounded faces extraction — powered by **CGAL** and **pybind11**, wrapped for Python.

---

## Features

- Weighted Voronoi diagram (Apollonius diagram)
- Extraction of only **bounded faces** (finite cells)
- Ready-to-use **Python bindings** via `pybind11`
- Built on **CGAL**, compiled as `.pyd` for Python
- Fast and robust geometric computation

---

## Requirements

- CMake 3.16+
- Python 3.8+
- MinGW-w64 (or MSVC)
- [vcpkg](https://github.com/microsoft/vcpkg) with:
  - `cgal`
  - `boost-algorithm`
  - `boost-system`
- [pybind11](https://github.com/pybind/pybind11) cloned locally

---

## How to Use

**Import the module:**
```python
from voronoi import weighted_voronoi as wv
```

**Build the weighted Voronoi (Apollonius) diagram:**
```python
cells = wv.build_apollonius_polygons(points, radii)
```

**Arguments:**

- `points`: list of 2D coordinates, e.g. `[(x1, y1), (x2, y2), ...]`
- `radii`: list of weights (same length as `points`), e.g. `[w1, w2, ...]`

**Returns:**

A list of `VoronoiCell` objects with:
- `.index`: index of the cell (int)
- `.boundary`: polygon boundary as list of `(x, y)` coordinates (list of tuples)
