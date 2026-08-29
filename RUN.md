# Jetson YOLO11 ROS2 Run Guide

## 1. 模型与类别

项目只使用以下两个类别，请勿修改名称或顺序：

```text
0 = mouse
1 = bottle
```

最终部署模型：

```text
/home/nvidia/jetson_yolo/best.pt
```

该模型来自训练结果 `train-6/best.pt`。

## 2. 独立摄像头检测

在 Jetson 终端执行：

```bash
cd ~/jetson_yolo
python3.10 detect.py
```

正常运行时会打开实时检测画面，显示类别、置信度、检测框和 FPS。Jetson 实测约 25–30 FPS。

## 3. 编译 ROS2 工作空间

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_yolo_ws
colcon build --symlink-install
source ~/ros2_yolo_ws/install/setup.bash
```

每次打开新终端，都需要重新执行两个 `source` 命令：

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_yolo_ws/install/setup.bash
```

## 4. 启动 YOLO ROS2 节点

第一个终端执行：

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_yolo_ws/install/setup.bash
ros2 run yolo_detector yolo_node
```

正常启动后应能看到模型加载信息，并确认类别为：

```text
{0: 'mouse', 1: 'bottle'}
```

## 5. 检查检测结果 topic

保持第一个终端运行，打开第二个终端：

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_yolo_ws/install/setup.bash
ros2 topic echo /detection_result
```

也可以先执行 `ros2 topic list`，列表中应包含 `/detection_result`。

## 6. 再次检查模型类别

```bash
cd ~/jetson_yolo
python3.10 -c "from ultralytics import YOLO; print(YOLO('best.pt').names)"
```

预期输出：

```text
{0: 'mouse', 1: 'bottle'}
```

## 7. 退出程序

在运行检测节点或 `ros2 topic echo` 的对应终端中按 `Ctrl+C`。如果同时运行了两个终端，需要分别退出。
