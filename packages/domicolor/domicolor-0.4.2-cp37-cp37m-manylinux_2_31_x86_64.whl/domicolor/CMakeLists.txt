cmake_minimum_required(VERSION 2.8.12)
project(domicolor_backend)

set(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -O0 -ggdb")
set(CMAKE_CXX_STANDARD 11)

add_subdirectory(pybind11)

pybind11_add_module(domicolor_backend cpp/domicolor_backend.cpp)
