import os
import cv2

# === 輸入與參數設定 ===
input_video_path = r"V000000094.mp4"  # << 影片路徑
output_dir = '3'

# 定義裁切比例（相對寬度）例如：left = 0.1, right = 0.9 代表裁掉左右 10%
"""
1, 2為left: 0.01 right: 0.6 top: 0 bottom: 1
3, 4為left: 0.01 right: 0.55 top: 0 bottom: 1
5, 6為left: 0.4 right: 0.95 top: 0 bottom: 0.85
"""
# 定義裁切比例（相對寬度和高度）
# 寬度裁切：left_ratio 和 right_ratio (0 到 1)
# 高度裁切：top_ratio 和 bottom_ratio (0 到 1)
crop_left_ratio = 0.01   # 左邊裁切比例
crop_right_ratio = 0.55   # 右邊裁切比例
crop_top_ratio = 0     # 上方裁切比例
crop_bottom_ratio = 1  # 下方裁切比例

# === 建立輸出資料夾 ===
os.makedirs(output_dir, exist_ok=True)
output_video_path = os.path.join(output_dir, os.path.basename(input_video_path))

# === 讀取影片資訊 ===
cap = cv2.VideoCapture(input_video_path)
if not cap.isOpened():
    raise FileNotFoundError(f"無法開啟影片：{input_video_path}")

fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# === 計算裁切像素 ===
# 寬度裁切
crop_left = int(frame_width * crop_left_ratio)
crop_right = int(frame_width * crop_right_ratio)
new_width = crop_right - crop_left

# 高度裁切
crop_top = int(frame_height * crop_top_ratio)
crop_bottom = int(frame_height * crop_bottom_ratio)
new_height = crop_bottom - crop_top

# === 檢查裁切範圍是否有效 ===
if new_width <= 0 or new_height <= 0:
    raise ValueError("裁切範圍無效，請檢查比例設定（裁切後寬度或高度小於等於0）")

# === 設定輸出影片參數 ===
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (new_width, new_height))
print(f"處理中的影像：{input_video_path}")
print(f"原始尺寸：{frame_width}x{frame_height}")
print(f"裁切區間：寬度 ({crop_left}, {crop_right}) -> 新寬度：{new_width}")
print(f"裁切區間：高度 ({crop_top}, {crop_bottom}) -> 新高度：{new_height}")

# === 開始逐幀處理 ===
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # 裁切寬度和高度
    cropped_frame = frame[crop_top:crop_bottom, crop_left:crop_right]
    out.write(cropped_frame)

# === 釋放資源 ===
cap.release()
out.release()

print(f"處理完成！輸出影片已儲存至：{output_video_path}")