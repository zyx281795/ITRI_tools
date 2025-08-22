import cv2
import os

# ======== 設定參數 ========
input_video_path = r"6.mp4"  # 影片路徑
output_frames_dir = r"frame_6"    # 輸出影格資料夾
frame_prefix = "frame_"                     # 影格檔名前綴

# ======== 創建輸出資料夾 ========
os.makedirs(output_frames_dir, exist_ok=True)

# ======== 讀取影片 ========
cap = cv2.VideoCapture(input_video_path)

if not cap.isOpened():
    raise IOError(f"無法開啟影片: {input_video_path}")

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # 儲存影格
    frame_filename = os.path.join(output_frames_dir, f"{frame_prefix}{frame_count:06d}.png")
    cv2.imwrite(frame_filename, frame)
    frame_count += 1

cap.release()
print(f"✅ 完成！共輸出 {frame_count} 張影格到 {output_frames_dir}")
