"""Assignment 2: subscribe to /camera/image_raw, run Canny, publish /camera/edges.

Complete the three TODOs. Test against the bag:
    ros2 bag play camera_bag --loop        (terminal 1)
    ros2 run edge_detector edge_detector_node   (terminal 2)
    ros2 topic hz /camera/edges            (terminal 3 — should show ~10 Hz)
"""
import rclpy
from rclpy.node import Node
# QoS helpers you may find useful:
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class EdgeDetector(Node):

    def __init__(self):
        super().__init__('edge_detector')
        self.bridge = CvBridge()

        EdgeDetectorQoS = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=5
        )

        # TODO(1): declare two integer parameters, 'canny_low' and 
        # 'canny_high', with self.declare_parameter(...). Find good values
        # through experimentation.

        # TODO(2): create the subscription to /camera/image_raw with
        # self.image_callback as the callback and using the EdgeDetectorQoS
        # for the QoS profile.

        self.subscription = None

        self.publisher = self.create_publisher(Image, '/camera/edges', 10)
        self.get_logger().info('edge_detector started')

    def image_callback(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        low = self.get_parameter('canny_low').value
        high = self.get_parameter('canny_high').value

        # TODO(3): convert `frame` to grayscale with cv2.cvtColor, then run
        # cv2.Canny(gray, low, high) to get a single-channel edge image.
        edges = None

        out = self.bridge.cv2_to_imgmsg(edges, encoding='mono8')
        out.header = msg.header
        self.publisher.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = EdgeDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
