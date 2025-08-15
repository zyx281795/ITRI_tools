import cv2
import os

# === 使用者參數設定 ===
input_video_path = '1.mp4'  # 修改為你的影片路徑
scale_factor = 2.0                   # 放大倍率，例如 2.0 為 2 倍

# === 輸出資料夾與檔案名稱 ===
output_dir = 'resized_video'
os.makedirs(output_dir, exist_ok=True)

# 讀取影片
cap = cv2.VideoCapture(input_video_path)
if not cap.isOpened():
    raise IOError(f"無法開啟影片：{input_video_path}")

# 原始影片資訊
fps = cap.get(cv2.CAP_PROP_FPS)
orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
new_width = int(orig_width * scale_factor)
new_height = int(orig_height * scale_factor)

# 產生輸出影片物件
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
basename = os.path.basename(input_video_path)
output_path = os.path.join(output_dir, f"resized_{basename}")
out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

print(f"開始處理影片：{input_video_path}")
print(f"原始解析度：{orig_width}x{orig_height} → 放大後：{new_width}x{new_height}")

# 處理每一幀
while True:
    ret, frame = cap.read()
    if not ret:
        break
    resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    out.write(resized_frame)

# 釋放資源
cap.release()
out.release()
print(f"影片儲存於：{output_path}")
