cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(PkgConfig)
pkg_check_modules(GDK_PIXBUF REQUIRED IMPORTED_TARGET gdk-pixbuf-2.0)
pkg_check_modules(LIBFFI REQUIRED IMPORTED_TARGET libffi)

add_executable(example example.cpp)
target_link_libraries(example ${CONAN_LIBS} PkgConfig::GDK_PIXBUF PkgConfig::LIBFFI)

message(STATUS "CONAN_LIBS ${CONAN_LIBS}")
