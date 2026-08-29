# Jetson YOLO11 ROS2 Object Detection

本项目在 Jetson 平台上使用 YOLO11n 完成 `mouse` 和 `bottle` 两类目标的实时检测，并通过 ROS2 发布检测结果。

## 项目结果

- 模型：YOLO11n
- 最终权重来源：`train-6/best.pt`
- 部署权重：`best.pt`
- 类别：`0 = mouse`，`1 = bottle`
- ROS2 topic：`/detection_result`
- Jetson 实测速度：约 25–30 FPS
- 实测截图：`test_results/test_01.png` 至 `test_results/test_20.png`

## 验证集指标

验证集共 65 images、91 instances。

| Class | Precision | Recall | mAP50 | mAP50-95 |
| --- | ---: | ---: | ---: | ---: |
| all | 0.988 | 1.000 | 0.989 | 0.872 |
| mouse | 0.977 | 1.000 | 0.984 | 0.853 |
| bottle | 0.999 | 1.000 | 0.995 | 0.890 |

## 文件说明

- `best.pt`：Jetson 部署使用的最终模型
- `detect.py`：独立摄像头检测程序
- `yolo_node.py`：ROS2 YOLO 检测节点
- `RUN.md`：完整运行与检查步骤
- `test_results/`：20 组 Jetson ROS2 实测截图及说明
- `ros2_detection.mp4`：ROS2 检测演示视频

## 快速运行

Jetson 独立检测：

```bash
cd ~/jetson_yolo
python3.10 detect.py
```

ROS2 节点的编译、启动、topic 检查和退出方法见 `RUN.md`。

## 验收结论

最终模型在验证集上取得 all mAP50 0.989、mAP50-95 0.872。Jetson 实测约 25–30 FPS，并能通过 `/detection_result` 发布检测结果。20 组实测覆盖单目标、双目标、负样本以及不同角度、距离和背景，满足项目实时检测与 ROS2 集成要求。
