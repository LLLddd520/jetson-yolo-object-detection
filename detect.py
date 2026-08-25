from ultralytics import YOLO
import cv2


# 加载训练好的模型
model = YOLO("best.pt")


# 打开外接摄像头
cap = cv2.VideoCapture(1)


# 获取摄像头分辨率
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# 创建视频保存对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(
    "result.mp4",
    fourcc,
    30,
    (width, height)
)


while True:

    # 读取一帧摄像头画面
    ret, frame = cap.read()

    if not ret:
        break


    # YOLO检测
    results = model(frame)


    # 绘制检测框、类别、置信度
    annotated_frame = results[0].plot()


    # 显示实时检测结果
    cv2.imshow(
        "YOLO Detection",
        annotated_frame
    )


    # 保存当前这一帧
    out.write(annotated_frame)


    # 按q退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# 释放资源
cap.release()
out.release()

cv2.destroyAllWindows()