// Assignment 2: subscribe to /camera/image_raw, run Canny, publish /camera/edges.
//
// Complete the three TODOs. Test against the bag:
//     ros2 bag play camera_bag --loop                  (terminal 1)
//     ros2 run edge_detector_cpp edge_detector_node    (terminal 2)
//     ros2 topic hz /camera/edges                      (terminal 3, ~10 Hz)

#include <memory>

#include <cv_bridge/cv_bridge.hpp>
#include <opencv2/imgproc.hpp>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/image.hpp>

class EdgeDetector : public rclcpp::Node {
public:
    EdgeDetector() : Node("edge_detector") {

        rclcpp::QoS EdgeDetectorQoS(rclcpp::KeepLast(5));
        EdgeDetectorQoS.reliable();
        EdgeDetectorQoS.transient_local();

        // TODO(1): declare two integer parameters, "canny_low" and
        // "canny_high", with this->declare_parameter(...). Find good values
        // through experimentation.

        // TODO(2): create the subscription to /camera/image_raw bound to
        // imageCallback and using EdgeDetectorQoS for the QoS profile.

        sub_ = nullptr;

        pub_ = this->create_publisher<sensor_msgs::msg::Image>(
            "/camera/edges", 10);

        RCLCPP_INFO(this->get_logger(), "edge_detector started");
    }

private:
    void imageCallback(
        const sensor_msgs::msg::Image::ConstSharedPtr msg) {

        const cv_bridge::CvImageConstPtr cv_in =
            cv_bridge::toCvShare(msg, "bgr8");

        const int low =
            this->get_parameter("canny_low").as_int();

        const int high =
            this->get_parameter("canny_high").as_int();

        cv::Mat edges;

        // TODO(3): convert cv_in->image to grayscale with cv::cvtColor,
        // then run cv::Canny with the two thresholds to fill `edges`.

        const cv_bridge::CvImage cv_out(
            msg->header, "mono8", edges);

        pub_->publish(*cv_out.toImageMsg());
    }

    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_;
    rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<EdgeDetector>());
    rclcpp::shutdown();
    return 0;
}