\# Jetson YOLO Object Detection with ROS2



基于 \*\*YOLO11n + NVIDIA Jetson + ROS2\*\* 的实时目标检测实验。



本项目完成了从数据采集、数据标注、YOLO 模型训练，到 Jetson 端部署、USB 摄像头实时检测以及 ROS2 检测结果发布的完整流程。



最终检测类别：



```text

0 = mouse

1 = bottle

```



\---



\## 1. 项目目标



本实验主要完成以下任务：



\- 构建 `mouse` 与 `bottle` 两类目标检测数据集

\- 使用 LabelImg 完成 YOLO 格式标注

\- 使用 YOLO11n 在 PC GPU 上训练模型

\- 将训练后的 `best.pt` 部署到 NVIDIA Jetson

\- 使用 USB 摄像头实现实时目标检测

\- 实时显示目标类别、检测框和置信度

\- 统计 Jetson 实时检测 FPS

\- 使用 ROS2 发布目标检测结果

\- 完成 20 组真实场景测试

\- 保存测试截图、模型和代码

\- 使用 GitHub 保存项目开发过程



整体流程：



```text

数据采集

&#x20;  ↓

LabelImg 标注

&#x20;  ↓

YOLO 数据集

&#x20;  ↓

PC 端 YOLO11n 训练

&#x20;  ↓

best.pt

&#x20;  ↓

传输至 Jetson

&#x20;  ↓

USB Camera

&#x20;  ↓

YOLO 实时推理

&#x20;  ↓

ROS2 Node

&#x20;  ↓

/detection\_result

```



\---



\# 2. Detection Classes



本项目包含两个目标类别：



| Class ID | Class Name |

|---:|---|

| 0 | mouse |

| 1 | bottle |



`data.yaml` 中类别配置：



```yaml

names:

&#x20; 0: mouse

&#x20; 1: bottle

```



LabelImg 的类别顺序也必须保持：



```text

mouse

bottle

```



即：



```text

0 = mouse

1 = bottle

```



\---



\# 3. Hardware Environment



\## 3.1 PC Training Platform



PC 主要用于：



\- 数据整理

\- 图像标注

\- YOLO11n 模型训练

\- 模型验证

\- Git / GitHub 项目管理



主要环境：



| Item | Configuration |

|---|---|

| OS | Windows |

| GPU | NVIDIA GeForce RTX 4060 Laptop GPU |

| GPU Memory | 8 GB |

| Python | 3.10.20 |

| PyTorch | 2.11.0+cu128 |

| Ultralytics | 8.4.127 |

| CUDA | Available |



GPU 检查：



```python

import torch



print(torch.cuda.is\_available())

print(torch.cuda.get\_device\_name(0))

```



正常输出：



```text

True

NVIDIA GeForce RTX 4060 Laptop GPU

```



\---



\## 3.2 Jetson Platform



模型最终部署于 NVIDIA Jetson。



Jetson 主要负责：



\- 加载 YOLO11n 模型

\- USB 摄像头采集

\- GPU 实时推理

\- 检测框绘制

\- 置信度显示

\- FPS 统计

\- ROS2 检测结果发布



Jetson 环境中已验证 CUDA 可用：



```bash

python3.10 -c "import torch; print(torch.cuda.is\_available())"

```



输出：



```text

True

```



Jetson CUDA 环境：



```text

CUDA 12.6

```



\---



\# 4. Dataset



数据集由自行采集的视频抽帧图片、拍摄图片以及后续补充样本组成。



主要包含：



\- 不同角度的 mouse

\- 不同距离的 mouse

\- 不同背景中的 mouse

\- 不同姿态的 bottle

\- 不同大小、外形和背景中的 bottle

\- 不同光照条件

\- 不同摄像头距离

\- 多种真实实验环境

\- 容易造成误识别的背景物体



后续测试发现部分长方形物体可能被误认为 bottle，因此进一步扩充了 bottle 样本，并加入更丰富的真实场景数据。



最终训练阶段额外加入了约 152 张 bottle 图片。



数据目录主要结构：



```text

object\_detection\_dataset/

│

├── raw\_images/

│

├── images/

│   ├── train/

│   └── val/

│

├── labels/

│   ├── train/

│   └── val/

│

├── data.yaml

│

└── runs/

```



最终验证集：



```text

Images: 65

Instances: 91

```



\---



\# 5. Data Annotation



标注工具：



```text

LabelImg

```



标注格式：



```text

YOLO

```



YOLO 标签格式：



```text

class\_id x\_center y\_center width height

```



例如：



```text

0 0.521 0.438 0.213 0.185

```



其中：



```text

0 = mouse

1 = bottle

```



在数据整理过程中曾检查并统一所有类别映射，保证整个数据集始终遵循：



```text

mouse  -> 0

bottle -> 1

```



\---



\# 6. Model



本项目使用：



```text

YOLO11n

```



选择 YOLO11n 的主要原因：



\- 模型参数量较小

\- 推理速度快

\- 适合 Jetson 边缘设备

\- GPU 占用较低

\- 能够满足实时目标检测需求

\- 对两类别检测任务性能充足



最终模型规模：



```text

Parameters: 2,582,542

GFLOPs: 6.4

```



\---



\# 7. PC Training



\## 7.1 Conda Environment



训练环境：



```text

object\_detection

```



激活：



```bat

conda activate object\_detection

```



进入数据集目录：



```bat

cd /d D:\\object\_detection\_dataset

```



\---



\## 7.2 Training Command



最终训练使用：



```bat

yolo detect train model=yolo11n.pt data=data.yaml epochs=100 imgsz=640 device=0

```



主要训练参数：



| Parameter | Value |

|---|---|

| Model | YOLO11n |

| Epochs | 100 |

| Image Size | 640 |

| Device | CUDA:0 |

| GPU | RTX 4060 Laptop GPU |

| Classes | 2 |



\---



\# 8. Final Training Results



最终模型来自：



```text

D:\\object\_detection\_dataset\\runs\\detect\\train-6\\weights\\best.pt

```



100 epochs 完成后最终验证结果：



| Class | Precision | Recall | mAP50 | mAP50-95 |

|---|---:|---:|---:|---:|

| all | 0.988 | 1.000 | 0.989 | 0.872 |

| mouse | 0.977 | 1.000 | 0.984 | 0.853 |

| bottle | 0.999 | 1.000 | 0.995 | 0.890 |



验证集：



```text

65 images

91 instances

```



模型速度：



```text

Preprocess:   0.2 ms

Inference:    3.3 ms

Postprocess:  1.0 ms

```



可以看到，两类目标在验证集上均获得较高检测性能。



其中：



```text

mouse Recall   = 1.000

bottle Recall  = 1.000

bottle mAP50   = 0.995

overall mAP50  = 0.989

```



\---



\# 9. PC Real-Time Detection



PC 端可使用摄像头进行实时测试。



基本流程：



```python

from ultralytics import YOLO

import cv2



model = YOLO("best.pt")



cap = cv2.VideoCapture(1)



while True:

&#x20;   ret, frame = cap.read()



&#x20;   if not ret:

&#x20;       break



&#x20;   results = model(frame)



&#x20;   annotated\_frame = results\[0].plot()



&#x20;   cv2.imshow(

&#x20;       "YOLO Detection",

&#x20;       annotated\_frame

&#x20;   )



&#x20;   if cv2.waitKey(1) \& 0xFF == 27:

&#x20;       break



cap.release()

cv2.destroyAllWindows()

```



\---



\# 10. Transfer Model to Jetson



最终模型复制到 Jetson：



```text

/home/nvidia/jetson\_yolo/best.pt

```



可以通过 SCP 从 PC 传输：



```bat

scp D:\\object\_detection\_dataset\\runs\\detect\\train-6\\weights\\best.pt nvidia@192.168.55.1:/home/nvidia/jetson\_yolo/best.pt

```



传输后检查模型类别：



```bash

python3.10 -c "from ultralytics import YOLO; m=YOLO('/home/nvidia/jetson\_yolo/best.pt'); print(m.names)"

```



正确输出：



```text

{0: 'mouse', 1: 'bottle'}

```



\---



\# 11. Jetson Camera Detection



进入 Jetson 项目：



```bash

cd \~/jetson\_yolo

```



启动摄像头检测：



```bash

python3.10 detect.py

```



Jetson 实时检测程序主要完成：



```text

USB Camera

&#x20;   ↓

Frame Capture

&#x20;   ↓

YOLO11n Inference

&#x20;   ↓

Bounding Box

&#x20;   ↓

Class

&#x20;   ↓

Confidence

&#x20;   ↓

FPS

```



\---



\# 12. ROS2 Integration



为了满足 ROS2 发布检测结果的实验要求，本项目创建了 ROS2 Python package：



```text

yolo\_detector

```



ROS2 工作空间：



```text

/home/nvidia/ros2\_yolo\_ws

```



主要目录：



```text

ros2\_yolo\_ws/

│

├── src/

│   └── yolo\_detector/

│       ├── package.xml

│       ├── setup.py

│       ├── setup.cfg

│       │

│       └── yolo\_detector/

│           ├── \_\_init\_\_.py

│           └── yolo\_node.py

│

├── build/

├── install/

└── log/

```



核心 ROS2 节点：



```text

yolo\_node.py

```



\---



\# 13. ROS2 Build



加载 ROS2：



```bash

source /opt/ros/humble/setup.bash

```



进入工作空间：



```bash

cd \~/ros2\_yolo\_ws

```



编译：



```bash

colcon build --symlink-install

```



加载工作空间：



```bash

source \~/ros2\_yolo\_ws/install/setup.bash

```



检查节点：



```bash

ros2 pkg executables yolo\_detector

```



正常输出：



```text

yolo\_detector yolo\_node

```



\---



\# 14. Run ROS2 YOLO Node



启动：



```bash

source /opt/ros/humble/setup.bash

source \~/ros2\_yolo\_ws/install/setup.bash



ros2 run yolo\_detector yolo\_node

```



正常启动信息：



```text

YOLO ROS2 detector started

Model classes: {0: 'mouse', 1: 'bottle'}

```



ROS2 节点完成：



\- 打开 USB Camera

\- 调用 YOLO11n

\- GPU 实时推理

\- 获取类别

\- 获取置信度

\- 获取检测框

\- 计算 FPS

\- 发布检测结果



\---



\# 15. ROS2 Topic



YOLO 识别结果发布到：



```text

/detection\_result

```



查看 topic：



```bash

ros2 topic list

```



正常输出：



```text

/detection\_result

/parameter\_events

/rosout

```



在第二个终端中：



```bash

source /opt/ros/humble/setup.bash

source \~/ros2\_yolo\_ws/install/setup.bash



ros2 topic echo /detection\_result

```



检测 mouse：



```text

data: mouse:0.64 | FPS:29.49

```



检测 bottle：



```text

data: bottle:0.86 | FPS:28.92

```



没有检测到目标：



```text

data: none | FPS:29.49

```



完整 ROS2 数据流：



```text

USB Camera

&#x20;    ↓

OpenCV

&#x20;    ↓

YOLO11n

&#x20;    ↓

Detection Results

&#x20;    ↓

ROS2 Publisher

&#x20;    ↓

/detection\_result

```



\---



\# 16. Confidence Threshold Optimization



在实际部署过程中发现，不同类别的检测难度并不完全相同。



因此最终 ROS2 程序采用了：



```text

YOLO 基础阈值

\+

分类别置信度阈值

```



的方式进行过滤。



其主要思想为：



```text

mouse  -> 独立 confidence threshold

bottle -> 独立 confidence threshold

```



这样可以：



\- 减少 mouse 漏检

\- 减少 bottle 误检

\- 根据真实场景调整检测灵敏度

\- 不需要重新修改模型权重



\---



\# 17. Jetson Real-Time Performance



Jetson 实际测试过程中实时 FPS 通常约：



```text

25–30 FPS

```



测试输出中曾达到：



```text

FPS: 29.49

```



实验实时性要求：



```text

>= 5 FPS

```



因此：



```text

25–30 FPS >> 5 FPS

```



能够满足实时目标检测要求。



\---



\# 18. 20-Group Real-World Test



完成模型部署后，在 Jetson + ROS2 环境中进行了 20 组实际检测。



测试内容覆盖：



\- mouse 单目标

\- bottle 单目标

\- mouse + bottle 双目标

\- 不同角度

\- 不同距离

\- 不同背景

\- 不同光照

\- 屏幕图片

\- 复杂背景

\- 负样本

\- 容易造成误检的物体



测试时同时记录：



```text

YOLO Detection Window

Detection Class

Confidence

FPS

ROS2 /detection\_result

```



\---



\# 19. Test Results



20 组测试截图保存在：



```text

test\_results/

```



截图可以用于验证：



\- USB 摄像头正常工作

\- Jetson GPU 推理正常

\- YOLO Detection Window 正常

\- mouse 能够识别

\- bottle 能够识别

\- 多目标能够同时识别

\- ROS2 topic 正常发布

\- 置信度能够实时输出

\- FPS 满足实验要求



\---



\# 20. Hard Negative Test



在早期测试中发现，模型偶尔会将类似电源适配器等长方形物体识别为 bottle。



例如：



```text

power adapter

&#x20;       ↓

false positive

&#x20;       ↓

bottle

```



因此进行了进一步的数据增强和重新训练。



主要改进包括：



\- 增加更多 bottle 正样本

\- 增加不同角度 bottle

\- 增加不同背景 bottle

\- 增加复杂场景

\- 测试容易与 bottle 混淆的物体

\- 调整分类别置信度阈值



最终使用新的训练模型进行 Jetson 实测。



\---



\# 21. Typical Problems and Improvements



\## 21.1 Mouse Missing Detection



部分环境中 mouse 曾出现短暂漏检。



可能原因：



\- 光照变化

\- mouse 与背景颜色接近

\- 摄像头距离变化

\- 目标尺寸过小

\- 摄像头角度变化



改进措施：



\- 增加 mouse 多角度样本

\- 增加不同背景样本

\- 调整 mouse confidence threshold

\- 增加真实 Jetson 摄像头场景数据



\---



\## 21.2 Bottle False Positive



早期模型曾出现：



```text

Power Adapter

→ bottle

```



这说明模型可能学习了过强的外形轮廓特征。



改进措施：



\- 增加 bottle 数据

\- 增加不同 bottle 外观

\- 增加负样本

\- 加入容易误识别的场景

\- 提高 bottle 独立置信度阈值

\- 重新训练模型



\---



\# 22. Repository Structure



GitHub 仓库主要结构：



```text

jetson-yolo-object-detection/

│

├── best.pt

│

├── detect.py

│

├── yolo\_node.py

│

├── README.md

│

├── result.mp4

│

├── test\_results/

│

└── runs/

```



主要文件说明：



\### `best.pt`



最终 YOLO11n 权重。



\---



\### `detect.py`



用于：



```text

Camera

→ YOLO

→ Bounding Box

→ Confidence

→ FPS

```



\---



\### `yolo\_node.py`



ROS2 YOLO 节点，用于：



```text

Camera

→ YOLO

→ Detection Result

→ ROS2 Publisher

→ /detection\_result

```



\---



\### `test\_results/`



保存 20 组真实 Jetson ROS2 检测截图。



\---



\# 23. Git / GitHub Development Record



本项目通过 Git 保存不同开发阶段。



主要开发过程：



```text

数据集创建

&#x20;   ↓

PC 模型训练

&#x20;   ↓

PC 实时检测

&#x20;   ↓

Jetson 模型部署

&#x20;   ↓

Jetson Camera Detection

&#x20;   ↓

ROS2 Integration

&#x20;   ↓

数据集扩充

&#x20;   ↓

模型重新训练

&#x20;   ↓

20 组测试

&#x20;   ↓

最终结果提交

```



GitHub commit 用于：



\- 记录实验过程

\- 保存重要版本

\- 记录个人开发贡献

\- 保存最终模型

\- 保存 ROS2 代码

\- 保存测试结果



\---



\# 24. Final Model Performance



最终模型：



```text

YOLO11n

```



最终验证性能：



| Metric | Result |

|---|---:|

| Precision | 0.988 |

| Recall | 1.000 |

| mAP50 | 0.989 |

| mAP50-95 | 0.872 |



分类结果：



| Class | P | R | mAP50 | mAP50-95 |

|---|---:|---:|---:|---:|

| mouse | 0.977 | 1.000 | 0.984 | 0.853 |

| bottle | 0.999 | 1.000 | 0.995 | 0.890 |



Jetson 实时速度：



```text

approximately 25–30 FPS

```



\---



\# 25. Experiment Requirement Completion



最终实验完成情况：



\- \[x] 至少两类目标

\- \[x] mouse 检测

\- \[x] bottle 检测

\- \[x] YOLO 数据集

\- \[x] LabelImg 标注

\- \[x] YOLO11n 模型训练

\- \[x] CUDA GPU 训练

\- \[x] PC 实时检测

\- \[x] Jetson 模型部署

\- \[x] Jetson GPU 推理

\- \[x] USB 摄像头

\- \[x] Bounding Box

\- \[x] Class

\- \[x] Confidence

\- \[x] FPS

\- \[x] ROS2 Node

\- \[x] ROS2 Topic

\- \[x] `/detection\_result`

\- \[x] 20 组真实场景测试

\- \[x] 测试截图

\- \[x] Git / GitHub 项目管理



\---



\# 26. Conclusion



本项目完成了从数据采集到 Jetson ROS2 部署的完整目标检测系统。



首先采集并标注 mouse 和 bottle 两类数据，随后使用 YOLO11n 在 RTX 4060 Laptop GPU 上完成模型训练。



最终模型在验证集上达到：



```text

Precision: 0.988

Recall:    1.000

mAP50:     0.989

mAP50-95:  0.872

```



模型随后部署到 NVIDIA Jetson，通过 USB 摄像头实现实时目标检测。



Jetson 实际运行速度约：



```text

25–30 FPS

```



明显高于实验要求的：



```text

5 FPS

```



进一步利用 ROS2 构建 `yolo\_detector` 节点，并通过：



```text

/detection\_result

```



实时发布：



\- Detection Class

\- Confidence

\- FPS



最终完成 20 组真实场景测试，并通过 GitHub 保存最终模型、代码和测试结果。



完整实验流程为：



```text

数据采集

&#x20;   ↓

数据标注

&#x20;   ↓

YOLO 数据集构建

&#x20;   ↓

YOLO11n 训练

&#x20;   ↓

模型验证

&#x20;   ↓

Jetson 部署

&#x20;   ↓

USB Camera

&#x20;   ↓

实时目标检测

&#x20;   ↓

ROS2 Node

&#x20;   ↓

/detection\_result

&#x20;   ↓

20 组真实场景测试

```



最终系统实现了较稳定的双类别实时目标检测，并完成了 Jetson 与 ROS2 的集成部署。

