cmake_minimum_required(VERSION 3.16)
project(ApolloniusVoronoi LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 1) Подключаем локальный pybind11 (папка с репо pybind11)
add_subdirectory("C:/libs/pybind11" "pybind11_build")

# 2) Находим CGAL (через vcpkg или системно)
find_package(CGAL REQUIRED)

# 3) Собираем библиотеку
add_library(weighted_voronoi SHARED src/weighted_voronoi.cpp)

target_link_libraries(weighted_voronoi
    PRIVATE
    CGAL::CGAL
    pybind11::module
)

# 4) Чтобы получить .pyd (Windows), а не .dll
set_target_properties(weighted_voronoi PROPERTIES
    PREFIX ""
    SUFFIX ".pyd"
)
