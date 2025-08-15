import cv2
import numpy as np
import os

# ======== 設定參數 ========
video_paths = [
    #video name, video script
    ("1.mp4", "origin 1080*1036"),
    ("2.mp4", "resize 1080*1036"),
    ("3.mp4", "Super-Resolution 1924*1072")
]
output_path = "2_SuperResolution_merged_cv2.mp4"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.0
font_color = (255, 255, 255)
font_thickness = 2
bg_color = (0, 0, 0)

# ======== 打開所有影片 ========
caps = [cv2.VideoCapture(path) for path, _ in video_paths]
if not all([cap.isOpened() for cap in caps]):
    raise RuntimeError("無法打開所有影片，請確認路徑正確")

# 獲取影片幀率與尺寸
fps = caps[0].get(cv2.CAP_PROP_FPS)
widths = [int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) for cap in caps]
heights = [int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) for cap in caps]
min_height = min(heights)

# 統一尺寸（高度一致）
def resize_frame(frame, target_height):
    h, w = frame.shape[:2]
    scale = target_height / h
    return cv2.resize(frame, (int(w * scale), target_height))

# 建立影片寫入器
total_width = sum([int(w * (min_height / h)) for w, h in zip(widths, heights)])
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_path, fourcc, fps, (total_width, min_height + 50))  # +50 留空間放文字

while True:
    rets_frames = [cap.read() for cap in caps]
    if not all([ret for ret, _ in rets_frames]):
        break

    # 調整尺寸與加入標籤
    labeled_frames = []
    for (_, label), (_, frame) in zip(video_paths, rets_frames):
        frame = resize_frame(frame, min_height)

        # 建立一個新的 frame，加上文字區塊
        label_area = np.full((50, frame.shape[1], 3), bg_color, dtype=np.uint8)
        cv2.putText(label_area, label, (10, 35), font, font_scale, font_color, font_thickness)
        combined = np.vstack([label_area, frame])
        labeled_frames.append(combined)

    # 水平合併所有影片
    final_frame = np.hstack(labeled_frames)
    out.write(final_frame)

# 清理
for cap in caps:
    cap.release()
out.release()
print(f"✅ 合併完成，儲存於：{output_path}")
