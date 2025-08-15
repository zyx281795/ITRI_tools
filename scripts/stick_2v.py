import cv2
import numpy as np
import os

# ======== 設定參數 ========
video_n = "3"
w = "SuperResolution"
video_path_1 = os.path.join("original", f"{video_n}.mp4")
video_path_2 = os.path.join("D:/work/2025_ITRI_Intern/working/video_compare/Turtle/Circle", f"{video_n}_output_{w}_result.mp4")
output_path = f"{video_n}_{w}_merged_cv2.mp4"
concat_mode = "horizontal"  # "horizontal" 或 "vertical"

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
font_color = (255, 255, 255)
bg_color = (0, 0, 0)
label_height = 50

labels = ["origin", f"{w}"]

# ======== 開啟影片 ========
cap1 = cv2.VideoCapture(video_path_1)
cap2 = cv2.VideoCapture(video_path_2)
if not cap1.isOpened() or not cap2.isOpened():
    raise RuntimeError("影片讀取失敗，請確認路徑正確")

fps = cap1.get(cv2.CAP_PROP_FPS)
w1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
h1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
w2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
h2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))

# ======== 統一尺寸 ========
if concat_mode == "horizontal":
    min_height = min(h1, h2)
    def resize(frame): return cv2.resize(frame, (int(frame.shape[1] * min_height / frame.shape[0]), min_height))
    output_size = (resize(np.zeros((h1, w1, 3))).shape[1] + resize(np.zeros((h2, w2, 3))).shape[1], min_height + label_height)
elif concat_mode == "vertical":
    min_width = min(w1, w2)
    def resize(frame): return cv2.resize(frame, (min_width, int(frame.shape[0] * min_width / frame.shape[1])))
    output_size = (min_width, resize(np.zeros((h1, w1, 3))).shape[0] + resize(np.zeros((h2, w2, 3))).shape[0] + 2 * label_height)
else:
    raise ValueError("concat_mode 必須是 'horizontal' 或 'vertical'")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, output_size)

# ======== 處理每一幀 ========
while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    if not ret1 or not ret2:
        break

    f1 = resize(frame1)
    f2 = resize(frame2)

    def add_label(frame, text):
        label_area = np.full((label_height, frame.shape[1], 3), bg_color, dtype=np.uint8)
        cv2.putText(label_area, text, (10, 35), font, font_scale, font_color, font_thickness)
        return np.vstack([label_area, frame])

    f1 = add_label(f1, labels[0])
    f2 = add_label(f2, labels[1])

    if concat_mode == "horizontal":
        merged = np.hstack([f1, f2])
    else:
        merged = np.vstack([f1, f2])

    out.write(merged)

# ======== 清理資源 ========
cap1.release()
cap2.release()
out.release()
print(f"✅ 影片合併完成：{output_path}")
