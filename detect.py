from ultralytics import YOLO
import cv2
import time

# =========================
# 1. 加载模型
# =========================
model = YOLO("best.pt")

# =========================
# 2. 分类别置信度阈值
# =========================
MOUSE_CONF = 0.20
BOTTLE_CONF = 0.55

# =========================
# 3. 打开摄像头
# =========================
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Camera 1 open failed, trying camera 0...")
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera open failed")
    exit()

print("Camera opened successfully")
print(f"Mouse threshold  : {MOUSE_CONF}")
print(f"Bottle threshold : {BOTTLE_CONF}")
print("Press ESC to exit")

# =========================
# 4. 实时检测
# =========================
while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to read camera frame")
        break

    start_time = time.time()

    # 必须低于 mouse 阈值
    # 否则 mouse 会在这里提前被 YOLO 删除
    results = model(
        frame,
        conf=0.15,
        device=0,
        verbose=False
    )

    result = results[0]

    # =========================
    # 5. 遍历检测结果
    # =========================
    for box in result.boxes:

        cls_id = int(box.cls[0])
        confidence = float(box.conf[0])

        # ---------- mouse ----------
        if cls_id == 0:

            if confidence < MOUSE_CONF:
                continue

            label_name = "mouse"

        # ---------- bottle ----------
        elif cls_id == 1:

            if confidence < BOTTLE_CONF:
                continue

            label_name = "bottle"

        else:
            continue

        # 获取边界框
        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0].tolist()
        )

        # 画框
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # 标签
        label = f"{label_name} {confidence:.2f}"

        cv2.putText(
            frame,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # =========================
    # 6. FPS
    # =========================
    elapsed = time.time() - start_time

    if elapsed > 0:
        fps = 1.0 / elapsed
    else:
        fps = 0.0

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # =========================
    # 7. 显示
    # =========================
    cv2.imshow(
        "YOLO Detection",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    # ESC退出
    if key == 27:
        break


# =========================
# 8. 释放资源
# =========================
cap.release()
cv2.destroyAllWindows()