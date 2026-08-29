import time
import cv2

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ultralytics import YOLO


class YoloDetector(Node):

    def __init__(self):
        super().__init__('yolo_detector')

        self.publisher_ = self.create_publisher(
            String,
            '/detection_result',
            10
        )

        self.model = YOLO(
            '/home/nvidia/jetson_yolo/best.pt'
        )

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise RuntimeError('Camera cannot be opened')

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.conf = 0.15
        self.imgsz = 640

        self.mouse_conf = 0.25
        self.bottle_conf = 0.40

        # 保存视频
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(
            '/home/nvidia/jetson_yolo/ros2_detection.mp4',
            fourcc,
            20.0,
            (640, 480)
        )

        self.frame_count = 0
        self.start_time = time.perf_counter()

        self.timer = self.create_timer(
            0.001,
            self.detect_callback
        )

        self.get_logger().info(
            'YOLO ROS2 detector started'
        )

        self.get_logger().info(
            f'Model classes: {self.model.names}'
        )

        self.get_logger().info(
            'Video saving to: /home/nvidia/jetson_yolo/ros2_detection.mp4'
        )

    def detect_callback(self):

        ok, frame = self.cap.read()

        if not ok:
            self.get_logger().warning(
                'Failed to read camera frame'
            )
            return

        results = self.model.predict(
            frame,
            device=0,
            imgsz=self.imgsz,
            conf=self.conf,
            verbose=False
        )

        result = results[0]

        detections = []

        for box in result.boxes:

            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            class_name = self.model.names[class_id]

            if class_name == 'mouse':
                if confidence < self.mouse_conf:
                    continue

            elif class_name == 'bottle':
                if confidence < self.bottle_conf:
                    continue

            detections.append(
                f'{class_name}:{confidence:.2f}'
            )

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = f'{class_name} {confidence:.2f}'

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        self.frame_count += 1

        elapsed = time.perf_counter() - self.start_time

        fps = (
            self.frame_count / elapsed
            if elapsed > 0
            else 0.0
        )

        cv2.putText(
            frame,
            f'FPS: {fps:.2f}',
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        msg = String()

        if detections:
            msg.data = (
                ', '.join(detections)
                + f' | FPS:{fps:.2f}'
            )
        else:
            msg.data = (
                f'none | FPS:{fps:.2f}'
            )

        self.publisher_.publish(msg)

        # 显示实时窗口
        cv2.imshow(
            'YOLO ROS2 Detection',
            frame
        )

        cv2.waitKey(1)

        # 保存视频
        self.video_writer.write(frame)

    def destroy_node(self):

        if self.cap.isOpened():
            self.cap.release()

        if self.video_writer.isOpened():
            self.video_writer.release()

        cv2.destroyAllWindows()

        super().destroy_node()


def main(args=None):

    rclpy.init(args=args)

    node = YoloDetector()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
