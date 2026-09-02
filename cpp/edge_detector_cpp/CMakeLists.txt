cmake_minimum_required(VERSION 3.8)
project(edge_detector_cpp)

set(CMAKE_CXX_STANDARD 17)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(OpenCV REQUIRED COMPONENTS core imgproc)

add_executable(edge_detector_node src/edge_detector_node.cpp)
ament_target_dependencies(edge_detector_node rclcpp sensor_msgs cv_bridge)
target_link_libraries(edge_detector_node ${OpenCV_LIBS})

install(TARGETS edge_detector_node DESTINATION lib/${PROJECT_NAME})

ament_package()
