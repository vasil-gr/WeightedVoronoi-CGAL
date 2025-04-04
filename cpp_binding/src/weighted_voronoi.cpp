#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>
#include <vector>
#include <utility>

#include <CGAL/Simple_cartesian.h>

#include <CGAL/Apollonius_graph_traits_2.h>
#include <CGAL/Apollonius_site_2.h>
#include <CGAL/Apollonius_graph_2.h>

#include <CGAL/Apollonius_graph_adaptation_traits_2.h>
#include <CGAL/Voronoi_diagram_2.h>

namespace py = pybind11;

typedef double Number_type;
typedef CGAL::Simple_cartesian<Number_type> Kernel_Exact;
// Traits + ApolloniusGraph + adapter
typedef CGAL::Apollonius_graph_traits_2<Kernel_Exact>     AGT2_K;
typedef CGAL::Apollonius_graph_2<AGT2_K>                  AG2;   // "ApolloniusGraph"
typedef CGAL::Apollonius_graph_adaptation_traits_2<AG2>   AG2_Trait;
typedef CGAL::Voronoi_diagram_2<AG2, AG2_Trait>  VD_AG2;
typedef AG2::Site_2              Site_2_Apo;
typedef Site_2_Apo::Point_2      Site_2_Point_2;
typedef Site_2_Apo::Weight       Site_2_Weight;

struct VoronoiCell {
    int index;  // cell index
    std::vector<std::pair<double,double>> boundary; // polygon vertices
};

// building Apollonius (weighted) diagram and extracting bounded faces
std::vector<VoronoiCell>
build_apollonius_polygons(
    const std::vector<std::pair<double,double>>& points,
    const std::vector<double>& radii
)
{
    if(points.size() != radii.size()){
        throw std::runtime_error("points.size() != radii.size()");
    }

    // sites
    std::vector<Site_2_Apo> nodes;
    nodes.reserve(points.size());
    for(size_t i=0; i<points.size(); i++){
        double x = points[i].first;
        double y = points[i].second;
        double w = radii[i];
        Site_2_Apo s(Site_2_Point_2(x, y), Site_2_Weight(w));
        nodes.push_back(s);
    }

    // 2) Voronoi Diagram from ApolloniusGraph
    VD_AG2 VDA; 
    VDA.clear();
    VDA.insert(nodes.begin(), nodes.end());

    // bounded faces
    std::vector<VoronoiCell> result;
    int idx = 0;

    // types
    typedef VD_AG2::Bounded_faces_iterator          BFI;
    typedef VD_AG2::Ccb_halfedge_circulator         HCirc;

    for(BFI f = VDA.bounded_faces_begin(); f != VDA.bounded_faces_end(); ++f){
        std::vector<std::pair<double,double>> poly;
        HCirc ec_start = f->ccb();
        HCirc ec = ec_start;

        do {
            auto p = ec->source()->point();  // CGAL point
            double px = CGAL::to_double(p.x());
            double py = CGAL::to_double(p.y());
            poly.push_back({px, py});
            ++ec;
        } while(ec != ec_start);

        VoronoiCell cell;
        cell.index = idx++;
        cell.boundary = poly;
        result.push_back(cell);
    }

    return result;
}

// PYBIND11_MODULE 
PYBIND11_MODULE(weighted_voronoi, m) {
    m.doc() = "Weighted Voronoi (Apollonius) via CGAL, following forum snippet";

    // class VoronoiCell
    py::class_<VoronoiCell>(m, "VoronoiCell")
        .def_readwrite("index", &VoronoiCell::index)
        .def_readwrite("boundary", &VoronoiCell::boundary);

    // func
    m.def("build_apollonius_polygons", 
          &build_apollonius_polygons,
          py::arg("points"),
          py::arg("radii"),
          R"pbdoc(
            Building Apollonius (weighted) diagram by Voronoi_diagram_2< Apollonius_graph_2 > 
            and extracting bounded faces.

            points: список ( (x,y), ... )
            radii: список ( w1, w2, ... )
            Returns: list of VoronoiCell (indexes and border coordinates).
          )pbdoc");
}
