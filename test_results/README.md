# Jetson ROS2 Real-World Test Results

本目录保存 20 组 Jetson + YOLO11n + ROS2 实际目标检测截图，文件为 `test_01.png` 至 `test_20.png`。

## 检测类别

```text
0 = mouse
1 = bottle
```

## ROS2 Topic

```text
/detection_result
```

## 实测性能

Jetson 实际检测速度约为 25–30 FPS，满足实时检测要求。

## 测试覆盖

20 组测试覆盖：

- mouse 单目标检测
- bottle 单目标检测
- mouse 与 bottle 双目标检测
- 负样本测试
- 不同角度
- 不同距离
- 不同背景与复杂场景

截图中可观察实时检测画面、边界框、类别、置信度、FPS，以及 ROS2 `/detection_result` 的发布结果。测试用于验证模型在 Jetson 实际环境中的目标检测能力和 ROS2 集成功能。
